# import asyncio

import uuid
from datetime import datetime

from django.db import models

# from asgiref.sync import sync_to_async
# from django.conf import settings
# logger = settings.LOGGER



class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)

    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(Course, self).save(*args, **kwargs)
        return self