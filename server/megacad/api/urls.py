from django.urls import path
from django.views.generic import TemplateView
from megacad.api.views import MessageView

app_name = "megacad"

urlpatterns = [
    path("", MessageView.as_view(), name="megacad"),
]
