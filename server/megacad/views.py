from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer


class MessageView(APIView):
    def get(self, request):
        output = [
            {
                "message": output.message,
                "user_id": output.department,
            }
            for output in Message.objects.all()
        ]
        return Response(output)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


# Create your views here.
# request-handler : actions
