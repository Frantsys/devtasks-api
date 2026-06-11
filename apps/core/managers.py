from django.db import models


class SoftDeleteQuerySet(models.QuerySet):

    def delete(self):
        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def alive(self):
        return self.get_queryset().alive()

    def deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=True)

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)
