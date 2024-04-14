import uuid
from datetime import datetime

from rest_framework import serializers

from .models import User


class UUIDField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return uuid.UUID(data)
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format.")


class DateTimeField(serializers.Field):
    def to_representation(self, value):
        return value.isoformat()

    def to_internal_value(self, data):
        try:
            return datetime.fromisoformat(data)
        except ValueError:
            raise serializers.ValidationError("Invalid datetime format.")
            

class EmailField(serializers.EmailField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            from django.core.validators import validate_email
            validate_email(data)
            return data
        except ValueError:
            raise serializers.ValidationError("Invalid email format.")


class ListField(serializers.ListField):
    child = serializers.UUIDField()

    def to_representation(self, value):
        return super().to_representation(value)

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class TextField(serializers.CharField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return str(data)



class UserSerializer(serializers.ModelSerializer):
    user_id = UUIDField(required=False)
    name = TextField(required=False)
    email = EmailField()
    password = TextField()
    role = TextField(required=False)
    created_at = DateTimeField(required=False)
    updated_at = DateTimeField(required=False)
    chat_ids = ListField(required=False)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'password', 'role', 'created_at', 'updated_at', 'chat_ids')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate_email(self, value):
        """
        Check that the email is not empty and doesn't already exist.
        """
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")

        existing_user = User.objects.filter(email=value).exists()
        if existing_user:
            raise serializers.ValidationError("Email already exists.")

        return value

    
    def validate_password(self, value):
        """
        Check that the password is not empty.
        """
        if not value:
            raise serializers.ValidationError("Password cannot be empty.")
        return value