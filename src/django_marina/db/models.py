from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy


class ProtectedModelMixin:
    """
    Add a method to disable the delete method of an instance.

    Override method `is_protected_against_deletion` to indicate that a delete should not be possible. Use case is
    when deletion may be allowed to a user (superuser, admin or otherwise), but cannot be executed because of
    objects that depend on this instance. In such a case, the foreign key relation to the model might benefit from
    `on_delete=models.PROTECT`.
    """

    # Default message shown to user if object is protected against deletion.
    protected_against_deletion_message = gettext_lazy("This object is protected against deletion.")

    @property
    def is_protected_against_deletion(self):
        """Return whether or not this object is protected against deletion."""
        return True

    def get_protected_against_deletion_message(self):
        """Return message shown to user if object is protected against deletion."""
        return self.protected_against_deletion_message

    def delete(self, *args, **kwargs):
        """Delete the instance, unless it is protected against deletion."""
        if not self.is_protected_against_deletion:
            return super().delete(*args, **kwargs)
        raise PermissionDenied(self.get_protected_against_deletion_message())
