# import asyncio

import uuid
from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField

# from asgiref.sync import sync_to_async
# from django.conf import settings
# logger = settings.LOGGER


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    chat_ids = ArrayField(ArrayField(models.IntegerField()), default=list)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(User, self).save(*args, **kwargs)
        return self
