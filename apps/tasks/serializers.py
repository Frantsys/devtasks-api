from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "description",
            "priority", "priority_display",
            "status", "status_display",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "is_deleted", "created_at", "updated_at",
            "priority_display", "status_display",
        ]
