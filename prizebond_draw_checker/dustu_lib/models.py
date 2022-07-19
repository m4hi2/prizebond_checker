from uuid import uuid4

from django.db import models
from django_extensions.db.models import TimeStampedModel


class UUIDModel(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid4, editable=False)

    def __str__(self) -> str:
        return str(self.uuid)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel, TimeStampedModel):
    class Meta:
        abstract = True
