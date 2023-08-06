from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT


__all__ = 'OnlyRelationMixin',


class OnlyRelationMixin:
    def __init__(self, *args, from_field=None, **kwargs):
        assert from_field is not None, (
            'Parameter `from_field` for underlying field is required.'
        )

        super().__init__(*args, **kwargs)

        self.from_field = from_field

        if (
            len(self.from_fields) == 1
            and
            self.from_fields[0] == RECURSIVE_RELATIONSHIP_CONSTANT
        ):
            self.from_fields = [self.from_field]

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=private_only)

        # For a real model we're removing actual field, but relation will
        # stay at it's place.
        # FIXME: Dunno how it will work for a table inheritance or some
        # other weird extending.
        if not cls._meta.abstract:
            for field in self.model._meta.local_fields:
                if field.name == self.name:
                    self.model._meta.local_fields.remove(field)

            # FIXME: This here is very tricky. May have some issues with it:
            self.name = self.from_field

    def contribute_to_related_class(self, cls, related):
        super().contribute_to_related_class(cls, related)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['from_field'] = self.from_field

        return name, path, args, kwargs
