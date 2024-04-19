from django.urls import path

from .views import (
    ChatCreateAPIView,
    ChatRetrieveAPIView,
    ChatDeleteAPIView,
    ChatListAPIView,
    ChatCompletionAPIView,
    ChatFeedbackUpdateAPIView,
)


app_name = "chat"

urlpatterns = [
    path(
        "create",
        ChatCreateAPIView.as_view(),
        name="chat-create",
    ),
    path(
        "<uuid:chat_id>",
        ChatCompletionAPIView.as_view(),
        name="chat-update",
    ),
    path(
        "<uuid:chat_id>/",
        ChatFeedbackUpdateAPIView.as_view(),
        name="chat-feedback-update",
    ),
    path(
        "<uuid:chat_id>/retrieve",
        ChatRetrieveAPIView.as_view(),
        name="chat-retrieve",
    ),
    path(
        "<uuid:chat_id>/delete",
        ChatDeleteAPIView.as_view(),
        name="chat-delete",
    ),
    path(
        "user/<uuid:user_id>",
        ChatListAPIView.as_view(),
        name="chat-list-by-user-id",
    ),
]
