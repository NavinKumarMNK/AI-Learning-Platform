import asyncio

import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

from asgiref.sync import sync_to_async
from django.conf import settings
logger = settings.LOGGER


class Chat(DjangoCassandraModel):
    chat_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(index=True)
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)
    messages = columns.List(columns.Map(columns.Text, columns.Text), default=list)
    title = columns.Text(max_length=128)

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        res = sync_to_async(super(Chat, self).save)(*args, **kwargs)
    
    async def append_message(self, message):
        """
        Appends a new message to the chat and returns the entire message list.
        """
        self.messages+=message  # Update sender based on request
        await self.save()
        return self.messages