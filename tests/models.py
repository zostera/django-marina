from django.db import models

from django_marina.db import ProtectedModelMixin


class ProtectedModel(ProtectedModelMixin, models.Model):
    name = models.CharField(max_length=10)
    is_delete_protected = models.BooleanField(default=True)

    @property
    def has_delete_protection(self):
        if self.is_delete_protected:
            return True
        return super().has_delete_protection
