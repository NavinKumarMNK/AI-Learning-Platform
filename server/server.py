#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import asyncio
import os

import django
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
User = get_user_model()


async def create_superuser():
    if not await User.objects.filter(username="admin").aexists():
        User.objects.filter(
            username=os.environ.get("DJANGO_ADMIN_USERNAME"),
        ).delete()
        User.objects.create_superuser(
            os.environ.get("DJANGO_ADMIN_USERNAME"),
            os.environ.get("DJANGO_ADMIN_EMAIL_ID"),
            os.environ.get("DJANGO_ADMIN_PASSWORD"),
        )


def main():
    try:
        from main.asgi import application
    except ImportError as exc:
        raise ImportError() from exc
    return application


loop = asyncio.get_event_loop()
loop.create_task(create_superuser())

app = main()
