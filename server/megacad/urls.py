from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from megacad.views import MessageView

app_name = "megacad"

urlpatterns = [
    path("api/", MessageView.as_view(), name="anything"),
    path("", TemplateView.as_view(template_name="index.html")),
]
