from django.urls import path

from .views import (
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserDeleteAPIView,
    UserListAPIView,
    UserUpdateAPIView,
)

app_name = "user"

urlpatterns = [
    path("",
        UserCreateAPIView.as_view(),
        name="user-create"
    ),
    path(
        "<uuid:user_id>",
        UserRetrieveAPIView.as_view(),
        name="user-retrieve",
    ),
    path(
        "<uuid:user_id>/update",
        UserUpdateAPIView.as_view(),
        name="user-update",
    ),
    path(
        "<uuid:user_id>/delete",
        UserDeleteAPIView.as_view(),
        name="user-delete",
    ),
    path(
        "users",
        UserListAPIView.as_view(),
        name="user-list",
    ),
]
