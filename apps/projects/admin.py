from django.contrib import admin
from .models import Sprint, Project


class SprintTasksInline(admin.TabularInline):
    model = Sprint.tasks.through
    extra = 0
    verbose_name = "Tarefa"
    verbose_name_plural = "Tarefas"


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "start_date", "end_date", "is_deleted", "created_at"]
    list_filter = ["status", "is_deleted"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
    inlines = [SprintTasksInline]
    exclude = ["tasks"]


class ProjectSprintsInline(admin.TabularInline):
    model = Project.sprints.through
    extra = 0
    verbose_name = "Sprint"
    verbose_name_plural = "Sprints"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "current_sprint", "is_deleted", "created_at"]
    list_filter = ["status", "is_deleted"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
    inlines = [ProjectSprintsInline]
    exclude = ["sprints"]
