from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy


class ProtectedModelMixin:
    """
    Add checks to update and delete methods of an instance.

    The use case is to protect against changes when update or delete is allowed for a user (superuser, admin or
    otherwise), but should not be executed because of objects that depend on this instance. In such a case, the foreign
    key relation to the model might benefit from `on_delete=models.PROTECT`.
    """

    # Default message shown to user when object has update protection.
    update_protection_message = gettext_lazy("This object has update protection.")

    # Default message shown to user when object has delete protection.
    delete_protection_message = gettext_lazy("This object has delete protection.")

    @property
    def has_update_protection(self):
        """Return whether this object has update protection."""
        return False

    def get_update_protection_message(self):
        """Return message shown to user when object has update protection."""
        return self.update_protection_message

    def save(self, *args, **kwargs):
        """Save the instance, unless it has a primary key and update protection."""
        if self.pk and self.has_update_protection:
            raise PermissionDenied(self.get_update_protection_message())
        return super().save(*args, **kwargs)

    @property
    def has_delete_protection(self):
        """Return whether this object has delete protection."""
        return False

    def get_delete_protection_message(self):
        """Return message shown to user when object has delete protection."""
        return self.delete_protection_message

    def delete(self, *args, **kwargs):
        """Delete the instance, unlessit has delete protection."""
        if self.has_delete_protection:
            raise PermissionDenied(self.get_delete_protection_message())
        return super().delete(*args, **kwargs)
