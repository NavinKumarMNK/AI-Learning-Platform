import uuid
from datetime import datetime

from rest_framework import serializers

from .models import Chat


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


class ListField(serializers.ListField):
    child = serializers.DictField(child=serializers.CharField())

    def to_representation(self, value):
        return super().to_representation(value)

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class TextField(serializers.CharField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return str(data)


class ChatSerializer(serializers.ModelSerializer):
    chat_id = UUIDField(required=False)
    user_id = UUIDField()
    created_at = DateTimeField(required=False)
    updated_at = DateTimeField(required=False)
    messages = ListField(required=False)
    title = TextField(required=False)

    class Meta:
        model = Chat
        fields = ["chat_id", "user_id", "created_at", "updated_at", "messages", "title"]

    def create(self, validated_data):
        return Chat.objects.create(**validated_data)

    def validate_user_id(self, value):
        """
        Check that the user_id is not empty.
        """
        if not value:
            raise serializers.ValidationError("User ID cannot be empty.")
        return value

    def validate_messages(self, value):
        """
        Check that messages is a list of dictionaries.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Messages must be a list.")
        for message in value:
            if not isinstance(message, dict):
                raise serializers.ValidationError("Each message must be a dictionary.")
        return value

    def validate_title(self, value):
        """
        Check that the title is not empty and its length is less than or equal to 128.
        """
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 128:
            raise serializers.ValidationError(
                "Title cannot be more than 128 characters."
            )
        return value
