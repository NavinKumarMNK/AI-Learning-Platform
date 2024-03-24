import asyncio

from django.http import StreamingHttpResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .models import Chat
from .serializers import ChatSerializer
from lib.ml_emb_service import get_embeddings


def qdrant(message_emb):
    return "Yo, Apples are red."

def llm(prompt):
    return "Red color bro"


class ChatCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

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


class ChatRetrieveAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ChatUpdateAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    def patch(self, request, *args, **kwargs):
        chat = self.get_object()
        message = request.data.get("messages")

        if message:
            message_emb = get_embeddings(message)
            message_related_content = qdrant(message_emb)

            # Generating prompt and getting response from llm
            prompt = "Related Content: " + message_related_content + "\n" + "Question: " + message[0].get("content")
            llm_response = llm(prompt)


            # Appending recevied message and llm message to database
            message+=[{"role": "AI", "content": llm_response}]
            chat_messages = chat.append_message(message)

            #sending response to user
            return Response(data={"messages": chat_messages})
        

        return Response(status=status.HTTP_400_BAD_REQUEST)
        # return self.partial_update(request, *args, **kwargs)
    
    # async def patch(self, request, *args, **kwargs):
    #     chat = self.get_object()
    #     message = request.data.get("messages")

    #     if message:
    #         task = asyncio.create_task(get_embeddings(message))
    #         message_emb = await task
    #         task = asyncio.create_task(qdrant(message_emb))
    #         message_related_content = await task

    #         # Generating prompt and getting response from llm
    #         prompt = "Related Content: " + message_related_content + "\n" + "Question: " + message[0].get("content")
    #         task = asyncio.create_task(llm(prompt))
    #         llm_response = await task


    #         # Appending recevied message and llm message to database
    #         message+=[{"role": "AI", "content": llm_response}]
    #         task = asyncio.create_task(chat.append_message(message))
    #         chat_messages = task

    #         #sending response to user
    #         return Response(data={"messages": chat_messages})
        

    #     return Response(status=status.HTTP_400_BAD_REQUEST)


class ChatDeleteAPIView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ChatListAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return Chat.objects.filter(user_id=user_id)
        else:
            return Chat.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
