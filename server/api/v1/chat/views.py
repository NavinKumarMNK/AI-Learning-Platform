import asyncio
import logging

from django.http import StreamingHttpResponse
from asgiref.sync import async_to_sync
from django.conf import settings

from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .models import Chat
from .serializers import ChatSerializer
from typing import Dict

from meglib.ml.store import VectorDB
from meglib.ml.api import Llm, Embedding

logger = logging.getLogger("django")
llm_api: Llm = settings.LLM_API
embed_api: Embedding = settings.EMBED_API
qdrant_db: VectorDB = settings.QDRANT_DB
qdrant_config: Dict = settings.QDRANT_CONFIG
llm_config: Dict = settings.LLM_CONFIG


class ChatCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @async_to_sync
    async def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        await self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        return_data = {"chat_id": data["chat_id"], "messages": data["messages"]}
        return Response(
            data=return_data, status=status.HTTP_201_CREATED, headers=headers
        )

    async def perform_create(self, serializer):
        serializer.save()


class ChatRetrieveAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    @async_to_sync
    async def get(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        logger.warning(response)
        return_data = {
            "messages": response.data["messages"],
            "title": response.data["title"],
        }
        return Response(
            return_data,
            status=status.HTTP_200_OK,
        )


class ChatCompletionAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    @async_to_sync
    async def post(self, request, *args, **kwargs):
        chat = self.get_object()
        payload: Dict = request.data
        messages = request.data["messages"]
        logger.info(payload)

        # retrieve embedding for message
        embedding_msg = ""
        for message in messages[:-3] or messages:
            embedding_msg += "\n" + message["content"].strip()

        embedding: Dict = await embed_api.query(
            payload={
                "data": embedding_msg,
                "type": "QUERY_EMBED",
            }
        )
        embedding = embedding["embedding"]

        # vector search
        retrieved_content: Dict = qdrant_db.proto_to_dict(
            await qdrant_db.search(
                collection_name=qdrant_config["main"]["collection_name"],
                vector=embedding,
                limit=qdrant_config["infer"]["limit"],
                filters={"course": payload["course"]},
            )
        )
        logger.info(retrieved_content)

        if "result" not in retrieved_content.keys():  # only contains time
            pass
        else:
            content = ""
            cont_no = 1
            for result in retrieved_content["result"]:
                score = result["score"]
                if score >= qdrant_config["infer"]["min_score"]:
                    content += (
                        f" \n{cont_no}. {result['payload']['text']['stringValue']}"
                    )
                    cont_no += 1

            if len(content) >= 1:
                messages[-1]["content"] = (
                    "Related Content: " + content + "\n" + messages[-1]["content"]
                )

        logger.info(messages)

        # llm generation
        payload = {
            "messages": messages,
            "stream": payload.get("stream", True),
            "max_tokens": llm_config.get("max_tokens", 1024),
            "temperature": llm_config.get("temperature", 0.7),
        }

        if payload.get("stream", True):
            llm_response = self._consume_and_append(
                llm_response=llm_api.query(payload=payload),
                chat=chat,
                messages=messages,
            )
            return StreamingHttpResponse(llm_response)

        else:
            llm_response = await llm_api.query_no_stream(payload=payload)
            message = {"role": "assistant", "content": content}
            messages.append(message)
            logger.info(messages)
            asyncio.create_task(chat.update_messages(messages))
            return Response(data={"messages": llm_response})

    async def _consume_and_append(self, llm_response, chat, messages):
        content = ""
        async for data in llm_response:
            content += data
            yield data

        message = {"role": "assistant", "content": content}
        messages.append(message)
        logger.info(messages)
        asyncio.create_task(chat.update_messages(messages))


class ChatDeleteAPIView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    @async_to_sync
    async def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ChatListAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        queryset = Chat.objects.filter(user_id=user_id)
        return queryset

    @async_to_sync
    async def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return_data = [
            {"chat_id": data["chat_id"], "title": data["title"]}
            for data in response.data
        ]
        return Response(
            return_data,
            status=status.HTTP_200_OK,
        )
