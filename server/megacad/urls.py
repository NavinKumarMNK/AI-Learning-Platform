from django.urls import path
from django.views.generic import TemplateView

from megacad.api.views import MessageView

app_name = "megacad"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
]
