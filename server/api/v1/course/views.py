import asyncio
import uuid

from django.http import StreamingHttpResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer
from megacad.api.mixins import StaffEditorPermissionMixin

# from asgiref.sync import sync_to_async, async_to_sync
# from django.conf import settings
# logger = settings.LOGGER


class CourseCreateAPIView(
    StaffEditorPermissionMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()


class CourseRetrieveAPIView(
    StaffEditorPermissionMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "course_id"

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        course = Course.objects.get(course_id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
        # return self.retrieve(request, *args, **kwargs)


class CourseUpdateMixinAPIView(
    StaffEditorPermissionMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "course_id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CourseDeleteAPIView(
    StaffEditorPermissionMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "course_id"

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CourseListAPIView(
    StaffEditorPermissionMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
