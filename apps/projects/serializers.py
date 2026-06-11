from rest_framework import serializers

from apps.tasks.serializers import TaskSerializer
from .models import Sprint, Project


class SprintSerializer(serializers.ModelSerializer):
    tasks_detail = TaskSerializer(source="tasks", many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = [
            "id", "title", "description", "tasks", "tasks_detail", "task_count",
            "start_date", "end_date", "status", "status_display",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "is_deleted", "created_at", "updated_at",
            "tasks_detail", "status_display", "task_count",
        ]

    def get_task_count(self, obj) -> int:
        return obj.tasks.filter(is_deleted=False).count()


class SprintWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            "id", "title", "description", "tasks",
            "start_date", "end_date", "status",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "is_deleted", "created_at", "updated_at"]

    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "A data de fim deve ser posterior à data de início."}
            )
        return attrs


class ProjectSprintInlineSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Sprint
        fields = ["id", "title", "status", "status_display", "start_date", "end_date"]


class ProjectSerializer(serializers.ModelSerializer):
    sprints_detail = ProjectSprintInlineSerializer(source="sprints", many=True, read_only=True)
    current_sprint_detail = ProjectSprintInlineSerializer(source="current_sprint", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    sprint_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "sprints", "sprints_detail", "sprint_count",
            "current_sprint", "current_sprint_detail", "status", "status_display",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "is_deleted", "created_at", "updated_at",
            "sprints_detail", "current_sprint_detail", "status_display", "sprint_count",
        ]

    def get_sprint_count(self, obj) -> int:
        return obj.sprints.filter(is_deleted=False).count()


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "sprints", "current_sprint", "status",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "is_deleted", "created_at", "updated_at"]

    def validate(self, attrs):
        current_sprint = attrs.get("current_sprint") or getattr(self.instance, "current_sprint", None)
        sprints = attrs.get("sprints")

        if current_sprint and sprints is not None:
            sprint_ids = [s.id for s in sprints]
            if current_sprint.id not in sprint_ids:
                raise serializers.ValidationError(
                    {"current_sprint": "O sprint atual deve estar na lista de sprints do projeto."}
                )
        return attrs
