import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
app = FastAPI()

__all__ = [app]
application = get_asgi_application()


app.mount("/static", StaticFiles(directory="staticfiles"), name="static")
app.mount("/", application)
