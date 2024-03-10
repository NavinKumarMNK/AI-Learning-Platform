import asyncio

from django.http import StreamingHttpResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .models import Chat
from .serializers import ChatSerializer


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


class ChatUpdateAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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
