# import asyncio

import uuid
from datetime import datetime

from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger("django")


class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # self.updated_at = timezone.now()
        super(Course, self).save(*args, **kwargs)
        return self
