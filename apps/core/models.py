import uuid

from django.db import models

from .managers import SoftDeleteManager


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em",
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Deletado",
        db_index=True,
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted", "updated_at"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
