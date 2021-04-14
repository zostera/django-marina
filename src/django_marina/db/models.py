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

    @classmethod
    def from_db(cls, db, field_names, values):
        """
        Store fields and values from database in instance for reference.

        Source: https://docs.djangoproject.com/en/3.1/ref/models/instances/#customizing-model-loading
        """
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def get_changed_fields(self, fields=None):
        """
        Return dictionary of fields with loaded values that have changed.

        :param fields: List of fields, defaults to all fields
        :return: Dictionary with fields and old values that have changed
        """
        if self._state.adding:
            return {}
        try:
            loaded_values = self._loaded_values
        except AttributeError:
            return {}
        if not fields:
            fields = list(loaded_values.keys())
        changed_fields = {}
        for field in fields:
            loaded_value = loaded_values[field]
            if getattr(self, field) != loaded_value:
                changed_fields[field] = loaded_value
        return changed_fields

    def has_changed_fields(self, fields=None):
        """
        Return whether any of the given fields (defaults to all fields) have changed.

        :param fields: List of fields, defaults to all fields
        :return: Bool whether or not any of the fields have changed
        """
        return bool(self.get_changed_fields(fields))

    @property
    def has_update_protection(self):
        """Return whether this object has update protection."""
        return False

    def get_update_protection_message(self):
        """Return message shown to user when object has update protection."""
        return self.update_protection_message

    def save(self, *args, **kwargs):
        """Save the instance, unless it has a primary key and update protection."""
        if self.has_update_protection and not self._state.adding:
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
