#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import asyncio
import os

import django
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from dotenv import load_dotenv
from utils.base import load_env

load_env()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
User = get_user_model()


async def create_superuser():
    if not await sync_to_async(User.objects.filter(username="admin").exists)():
        await sync_to_async(
            User.objects.filter(username=os.environ.get("DJANGO_ADMIN_USERNAME")).delete
        )()
        await sync_to_async(User.objects.create_superuser)(
            os.environ.get("DJANGO_ADMIN_USERNAME"),
            os.environ.get("DJANGO_ADMIN_EMAIL_ID"),
            os.environ.get("DJANGO_ADMIN_PASSWORD"),
        )


def main():
    try:
        from main.asgi import app
    except ImportError as exc:
        raise ImportError() from exc
    return app


loop = asyncio.get_event_loop()
loop.create_task(create_superuser())
app = main()
