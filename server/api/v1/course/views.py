import asyncio
import uuid
import logging
import os

from django.core.files.storage import FileSystemStorage
from django.http import StreamingHttpResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Course
from .serializers import CourseSerializer
from megacad.api.mixins import StaffEditorPermissionMixin

from asgiref.sync import sync_to_async, async_to_sync
from django.conf import settings

from meglib.ml.store import VectorDB
from meglib.ml.api import Embedding
from meglib.ml.loaders import PDFLoader
from meglib.ml.preprocessor import DocumentProcessor
from meglib.ml.errors import PDFError

from typing import Dict

logger = logging.getLogger("django")
embed_api: Embedding = settings.EMBED_API
qdrant_db: VectorDB = settings.QDRANT_DB
doc_proc: DocumentProcessor = settings.DOC_PROCESSOR
pdf_loader: PDFLoader = settings.PDF_LOADER
temp_storage: FileSystemStorage = settings.STORAGES["temp_storage"]["BACKEND"]
qdrant_config: Dict = settings.QDRANT_CONFIG
doc_proc_config: Dict = settings.DOC_PROC_CONFIG


class CourseCreateAPIView(
    # StaffEditorPermissionMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @async_to_sync
    async def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await sync_to_async(self.perform_create)(serializer)
        headers = self.get_success_headers(serializer.data)
        return_data = {"course_id": serializer.data["course_id"]}
        return Response(
            data=return_data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer: CourseSerializer):
        serializer.save()


class CourseRetrieveAPIView(
    # StaffEditorPermissionMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "course_id"

    @async_to_sync
    async def get(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        course = await Course.objects.aget(course_id=course_id)
        serializer = CourseSerializer(course)
        return_data = {
            "name": serializer.data["name"],
            "description": serializer.data["description"],
            "instructor_name": serializer.data["instructor_name"],
        }
        return Response(data=return_data)


class CourseUpdateMixinAPIView(
    # StaffEditorPermissionMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "course_id"

    @async_to_sync
    async def patch(self, request: Request, *args, **kwargs) -> Response:
        return await sync_to_async(self.partial_update)(request, *args, **kwargs)


class CourseDeleteAPIView(
    # StaffEditorPermissionMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "course_id"

    @async_to_sync
    async def delete(self, request: Request, *args, **kwargs) -> Response:
        return await sync_to_async(self.destroy)(request, *args, **kwargs)


class CourseDocumentUploadAPIView(
    # StaffEditorPermissionMixin,
    generics.GenericAPIView,
):
    def _get_batches(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    async def _process_file(self, file_path: str, meta_data: Dict, course_id):
        documents = pdf_loader.parse_document(path=file_path, meta_data=meta_data)
        proc_docs = []
        meta_data = []
        for raw_doc in documents:
            for doc in doc_proc.recursive_split_overlap(
                document=raw_doc,
                min_size=doc_proc_config["min_size"],
                overlap=doc_proc_config["overlap"],
            ):
                proc_docs.append(doc.page_content)
                meta_data.append(doc.metadata)

        vector_batch = []
        for batch in self._get_batches(
            proc_docs, doc_proc_config["embed_max_batch_size"]
        ):
            response = await embed_api.query(
                payload={"type": "PASSAGE_EMBED", "data": batch}
            )
            vector_batch.extend(response["embedding"])

        await qdrant_db.insert(
            collection_name=qdrant_config["main"]["collection_name"],
            data=[
                {
                    "vector": vector,
                    "payload": {
                        "content": page_content,
                        "course_id": str(course_id),
                        "metadata": metadata,
                    },
                }
                for page_content, vector, metadata in zip(
                    proc_docs, vector_batch, meta_data
                )
            ],
            wait=False,
        )
        os.remove(file_path)

        return len(vector_batch)

    @async_to_sync
    async def post(self, request: Request, *args, **kwargs) -> Response:
        file = request.FILES.get("file")
        course_id = kwargs["course_id"]
        try:
            meta_data = {
                "start_page": int(request.data.get("start_pg_no")),
                "end_page": int(request.data.get("end_pg_no")),
            }
        except Exception:
            return Response(
                {"status": "meta data should contain valid page numbers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not file:
            return Response(
                {"status": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            file_ext = file.name.split(".")[-1]
            if file_ext != "pdf":
                return Response(
                    {"status": "Upload only pdf file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            filename = f"{uuid.uuid4()}.{file_ext}"
            temp_storage.save(filename, file)

            num_splits = await self._process_file(
                os.path.join(temp_storage.base_location, filename),
                meta_data=meta_data,
                course_id=course_id,
            )

            return Response(
                data={
                    "status": f"Successfully File got processed and saved into {num_splits} splits"
                },
                status=status.HTTP_200_OK,
            )

        except PDFError as e:
            return Response(
                data={"status": e.message}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as err:
            logger.error(err)
            import traceback

            traceback.print_exc()

            return Response(
                {"status": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
