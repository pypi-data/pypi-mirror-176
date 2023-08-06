from typing import Any, Dict, Tuple

from django.db import models


LoadedFieldValues = Dict[str, Any]
ChangedFieldValues = Dict[str, Tuple[Any, Any]]


class ChangedFieldValuesModelMixin:
    """Mixin to keep track of changed field values.

    All changes (since loading the model from the database) are available
    in the `changed_field_values` property. The property contains a mapping
    where the key is the changed field name and the value a tuple of the old
    and new field value.

    To just check if a field was changed use the `in` operator:
    >>> 'field_name' in self.changed_field_values
    """

    _loaded_values: LoadedFieldValues

    @classmethod
    def from_db(cls, db, field_names, values) -> models.Model:
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    @property
    def changed_field_values(self) -> ChangedFieldValues:
        changes = {}
        for field_name, old_value in getattr(self, '_loaded_values', {}).items():
            new_value = getattr(self, field_name)
            if old_value != new_value:
                changes[field_name] = (old_value, new_value)
        return changes
