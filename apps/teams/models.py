from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Team(BaseModel):
    sector = models.CharField(
        max_length=255,
        verbose_name="Setor",
        help_text="Nome ou área da equipe (ex: Backend, QA, Design).",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"

    def __str__(self):
        return self.sector


class TeamMember(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships",
        verbose_name="Usuário",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Equipe",
    )
    role = models.CharField(
        max_length=100,
        verbose_name="Papel",
        help_text="Papel do membro na equipe (ex: Tech Lead, Dev, Designer).",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Membro de Equipe"
        verbose_name_plural = "Membros de Equipe"
        unique_together = [("user", "team")]

    def __str__(self):
        return f"{self.user} → {self.team} [{self.role}]"
