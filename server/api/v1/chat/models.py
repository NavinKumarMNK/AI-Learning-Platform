import asyncio

import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

from asgiref.sync import sync_to_async
from django.conf import settings


class Chat(DjangoCassandraModel):
    chat_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(index=True)
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)
    messages = columns.List(columns.Map(columns.Text, columns.Text), default=list)
    title = columns.Text(max_length=128)
    feedback = columns.TinyInt(default=0)

    async def async_save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Chat, self).save(*args, **kwargs)

    async def update_messages(self, message):
        """Appends a new message to the chat and returns the entire message list."""
        self.messages = message
        await self.async_save()
