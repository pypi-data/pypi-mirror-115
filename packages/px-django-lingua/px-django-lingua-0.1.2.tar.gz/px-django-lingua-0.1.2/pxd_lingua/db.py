from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor


__all__ = 'OnlyRelationMixin', 'TranslatedRelationField',


class OnlyRelationMixin:
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

    def contribute_to_related_class(self, cls, related):
        print('shitt')
        print(self, cls, related)
        super().contribute_to_related_class(cls, related)


# class (ReverseOneToOneDescriptor):


class TranslatedRelationField(OnlyRelationMixin, models.OneToOneField):
    related_accessor_class = ReverseOneToOneDescriptor

    def get_forward_related_filter(self, obj):
        """
        Return the keyword arguments that when supplied to
        self.model.object.filter(), would select all instances related through
        this field to the remote obj. This is used to build the querysets
        returned by related descriptors. obj is an instance of
        self.related_field.model.
        """
        print('apshit', obj)
        return {
            '%s__%s' % (self.name, rh_field.name): getattr(obj, rh_field.attname)
            for _, rh_field in self.related_fields
        }
