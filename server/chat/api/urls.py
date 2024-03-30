from django.urls import path

from .views import (
    ChatCreateAPIView,
    ChatDeleteAPIView,
    ChatListAPIView,
    ChatUpdateAPIView,
)

app_name = "chat"

urlpatterns = [
    path(
        "<uuid:chat_id>/",
        ChatUpdateAPIView.as_view(),
        name="chat-update",
    ),
    path(
        "<uuid:chat_id>/",
        ChatDeleteAPIView.as_view(),
        name="chat-delete",
    ),
    path(
        "user/<uuid:user_id>/",
        ChatListAPIView.as_view(),
        name="chat-list-by-user-id",
    ),
    path("", ChatCreateAPIView.as_view(), name="chat-create"),
]
