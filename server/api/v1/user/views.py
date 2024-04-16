import asyncio

from django.http import StreamingHttpResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from megacad.api.mixins import StaffEditorPermissionMixin

# from asgiref.sync import sync_to_async, async_to_sync
# from django.conf import settings
# logger = settings.LOGGER


class UserCreateAPIView(
    StaffEditorPermissionMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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


class UserRetrieveAPIView(
    StaffEditorPermissionMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserUpdateAPIView(
    StaffEditorPermissionMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDeleteAPIView(
    StaffEditorPermissionMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserListAPIView(
    StaffEditorPermissionMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
