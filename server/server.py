#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import asyncio
import os
import django

from uvicorn import Config, Server
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from utils.base import load_env

from django.conf import settings
from meglib.ml.store import VectorDB
from typing import Dict
import random

load_env()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
User = get_user_model()

qdrant_db: VectorDB = settings.QDRANT_DB
qdrant_config: Dict = settings.QDRANT_CONFIG


async def create_main_qdrant_collection():
    if not await qdrant_db.verify(
        collection_name=qdrant_config["main"]["collection_name"]
    ):
        return await qdrant_db.create(
            collection_name=qdrant_config["main"]["collection_name"],
            dim=1024,
            distance="cosine",
            timeout=5,
        )
    if os.environ.get("DEBUG"):
        await qdrant_db.insert(
            collection_name=qdrant_config["main"]["collection_name"],
            data=[
                {
                    "vector": [
                        random.random() for x in range(qdrant_config["main"]["dim"])
                    ],
                    "payload": {"text": "Hi, This is Megacad", "course": "general"},
                },
            ],
        )


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
loop.create_task(create_main_qdrant_collection())
app = main()
