from django.db import models

from apps.core.models import BaseModel
from apps.tasks.models import Task


class SprintStatusChoices(models.TextChoices):
    NOT_STARTED = "not_started", "Não Iniciada"
    IN_PROGRESS = "in_progress", "Em Progresso"
    DONE = "done", "Concluída"


class ProjectStatusChoices(models.TextChoices):
    PAUSED = "paused", "Pausado"
    ACTIVE = "active", "Ativo"
    DONE = "done", "Concluído"
    CLOSED = "closed", "Encerrado"


class Sprint(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(blank=True, default="", verbose_name="Descrição")
    tasks = models.ManyToManyField(Task, blank=True, related_name="sprints", verbose_name="Tarefas")
    start_date = models.DateField(verbose_name="Data de início")
    end_date = models.DateField(verbose_name="Data de fim")
    status = models.CharField(
        max_length=15,
        choices=SprintStatusChoices.choices,
        default=SprintStatusChoices.NOT_STARTED,
        verbose_name="Status",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Sprint"
        verbose_name_plural = "Sprints"

    def __str__(self):
        return f"{self.title} ({self.start_date} → {self.end_date})"


class Project(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(blank=True, default="", verbose_name="Descrição")
    sprints = models.ManyToManyField(Sprint, blank=True, related_name="projects", verbose_name="Sprints")
    current_sprint = models.ForeignKey(
        Sprint,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="current_in_projects",
        verbose_name="Sprint atual",
    )
    status = models.CharField(
        max_length=10,
        choices=ProjectStatusChoices.choices,
        default=ProjectStatusChoices.ACTIVE,
        verbose_name="Status",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]" # type: ignore
