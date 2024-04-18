import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from chat.chainlit import chainlit_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
app = FastAPI()
## hello

django_app = get_asgi_application()

# app.mount("/chat", chainlit_app)
app.mount("/static", StaticFiles(directory="staticfiles"), name="static")
app.mount("/", django_app)

__all__ = [app]
