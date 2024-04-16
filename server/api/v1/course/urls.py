from django.urls import path


from .views import (
    CourseCreateAPIView,
    CourseRetrieveAPIView,
    CourseDeleteAPIView,
    CourseListAPIView,
    CourseUpdateMixinAPIView,
)

app_name = "api.v1.course"

urlpatterns = [
    path("", CourseCreateAPIView.as_view(), name="course-create"),
    path(
        "<uuid:course_id>",
        CourseRetrieveAPIView.as_view(),
        name="course-retrieve",
    ),
    path(
        "<uuid:course_id>/update",
        CourseUpdateMixinAPIView.as_view(),
        name="course-update",
    ),
    path(
        "<uuid:course_id>/delete",
        CourseDeleteAPIView.as_view(),
        name="course-delete",
    ),
    path(
        "courses",
        CourseListAPIView.as_view(),
        name="course-list",
    ),
]
