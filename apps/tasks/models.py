from django.db import models

from apps.core.models import BaseModel


class PriorityChoices(models.TextChoices):
    LOW = "low", "Baixa"
    MEDIUM = "medium", "Média"
    HIGH = "high", "Alta"


class StatusChoices(models.TextChoices):
    NOT_STARTED = "not_started", "Não Iniciada"
    IN_PROGRESS = "in_progress", "Em Progresso"
    DONE = "done", "Concluída"


class Task(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(blank=True, default="", verbose_name="Descrição")
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        verbose_name="Prioridade",
    )
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.NOT_STARTED,
        verbose_name="Status",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title} ({self.get_status_display()})"
