import asyncio

from django.http import StreamingHttpResponse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.views import APIView


class ChatApiView(APIView):
    def get(self, request):
        async def event_stream():
            try:
                for number in range(1, 3):
                    yield f"data: {number}\n\n"
                    await asyncio.sleep(1)  # Asynchronous delay
            except Exception as e:
                # Handle exceptions (e.g., yield an error message or special event)
                print(f"Error in event stream: {e}")

        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
