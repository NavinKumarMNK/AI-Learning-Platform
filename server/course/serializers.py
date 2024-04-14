import uuid
from datetime import datetime

from rest_framework import serializers

from .models import Course


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
            


class TextField(serializers.CharField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return str(data)
    




class CourseSerializer(serializers.ModelSerializer):
    course_id = UUIDField(required=False)
    name = TextField()
    description = TextField(required=False)
    instructor_name = TextField(required=False)
    created_at = DateTimeField(required=False)
    updated_at = DateTimeField(required=False)

    class Meta:
        model = Course
        fields = ('course_id', 'name', 'description', 'instructor_name', 'created_at', 'updated_at')


    def validate_name(self, value):
        """
        Check that the name is not empty and doesn't already exist.
        """
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")

        existing_course = Course.objects.filter(name=value).exists()
        if existing_course:
            raise serializers.ValidationError("Course name already exists.")

        return value