from django.urls import path
from django.views.generic import TemplateView
from megacad.api.views import MessageView

urlpatterns = [
    path("", MessageView.as_view()),
]
