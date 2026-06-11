from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "priority", "status", "is_deleted", "created_at"]
    list_filter = ["priority", "status", "is_deleted"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
