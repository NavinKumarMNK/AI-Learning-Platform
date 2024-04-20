from django.urls import path


from .views import (
    CourseCreateAPIView,
    CourseRetrieveAPIView,
    CourseDeleteAPIView,
    CourseUpdateMixinAPIView,
    CourseDocumentUploadAPIView,
)

app_name = "api.v1.course"

urlpatterns = [
    path(
        "create",
        CourseCreateAPIView.as_view(),
        name="course-create",
    ),
    path(
        "<uuid:course_id>/upload",
        CourseDocumentUploadAPIView.as_view(),
        name="course-upload",
    ),
    path(
        "<uuid:course_id>/retrieve",
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
]
