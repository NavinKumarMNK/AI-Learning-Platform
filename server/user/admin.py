from django.contrib import admin

# Register your models here.

from .api.models import User

admin.site.register(User)