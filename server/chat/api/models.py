import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class Chat(DjangoCassandraModel):
    chat_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(index=True)
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)
    messages = columns.List(columns.Map(columns.Text, columns.Text), default=list)
    title = columns.Text(max_length=128)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(Chat, self).save(*args, **kwargs)
        return self
    
    def append_message(self, message):
        """
        Appends a new message to the chat and returns the entire message list.
        """
        self.messages+=message  # Update sender based on request
        self.save()
        return self.messages