from chat.api.views import ChatApiView
from django.urls import path

app_name = "chat"

urlpatterns = [path("", view=ChatApiView.as_view())]
