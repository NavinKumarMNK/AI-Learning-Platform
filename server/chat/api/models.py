import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from django.db import models
from django_cassandra_engine.models import DjangoCassandraModel


class ChatMessage(DjangoCassandraModel):
    message_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    content = columns.Text()
