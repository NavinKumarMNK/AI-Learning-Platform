from django.db import models


class Message(models.Model):
    message: str = models.CharField(max_length=512)
    user_id: str = models.CharField(max_length=32)
