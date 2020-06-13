from django.db import models

from django_marina.db.models import ProtectedModelMixin


class ProtectedModel(ProtectedModelMixin, models.Model):
    name = models.CharField(max_length=10)
    is_protected = models.BooleanField(default=True)

    @property
    def is_protected_against_deletion(self):
        if not self.is_protected:
            return False
        return super().is_protected_against_deletion
