from typing import Dict, Optional, Type
from django.db import models
from django.db.models.fields.related_descriptors import (
    ReverseOneToOneDescriptor
)
from django.db.models.fields.related import OneToOneRel

from .exceptions import UnsavedLanguageControlAttempt
from .loader import RelationStorage
from .utils import LanguageGetterMixin, is_translation
from .db import OnlyRelationMixin


__all__ = (
    'MAGIC_TRANSLATION_ENTITY_FIELD',
    'MAGIC_TRANSLATION_STORED_FIELD',
    'MAGIC_TRANSLATION_CONTROL_FIELD',

    'TranslatedRelationField',
    'apply_magic_to_translation_model',
)

MAGIC_TRANSLATION_ENTITY_FIELD: str = 'entity'
MAGIC_TRANSLATION_STORED_FIELD: str = 'translated'
MAGIC_TRANSLATION_CONTROL_FIELD: str = 'language'


class TranslatedRelationDescriptor(
    LanguageGetterMixin, ReverseOneToOneDescriptor
):
    related: OneToOneRel

    def get_queryset(self, language: Optional[str] = None, **hints):
        language = language if language is not None else self.get_language()

        return super().get_queryset(**hints).by_language(language)

    def __get__(self, instance, cls=None) -> models.Model:
        try:
            return super().__get__(instance, cls=None)
        except self.RelatedObjectDoesNotExist:
            return instance

    def __set__(self, instance, value):
        # FIXME: Copypasted method from super because of related model check.
        # Maybe there is a way of not doing this.
        # Also in this method I removed database save mechanics, as there
        # is nothing to save here. Perhaps this could be done in som other
        # way. Think of it.

        if value is None:
            # Update the cached related instance (if any) & clear the cache.
            # Following the example above, this would be the cached
            # ``restaurant`` instance (if any).
            rel_obj = self.related.get_cached_value(instance, default=None)
            if rel_obj is not None:
                # Remove the ``restaurant`` instance from the ``place``
                # instance cache.
                self.related.delete_cached_value(instance)
                # Set the ``place`` field on the ``restaurant``
                # instance to None.
                setattr(rel_obj, self.related.field.name, None)
        elif not isinstance(value, (self.related.related_model, self.related.model)):
            raise ValueError(
                'Cannot assign "%r": "%s.%s" must be a "%s" instance.' % (
                    value,
                    instance._meta.object_name,
                    self.related.get_accessor_name(),
                    self.related.related_model._meta.object_name,
                )
            )
        else:
            self.related.set_cached_value(instance, value)


class TranslatedRelationField(OnlyRelationMixin, models.OneToOneField):
    related_accessor_class = TranslatedRelationDescriptor


class LanguageController(LanguageGetterMixin):
    instance: models.Model
    descriptor: 'LanguageControlDescriptor'
    translated_descriptor: 'TranslatedRelationDescriptor'
    storage: RelationStorage
    code: Optional[str]

    def __init__(
        self,
        instance: models.Model,
        descriptor: 'LanguageControlDescriptor',
        storage: Optional[RelationStorage] = None
    ):
        self.instance = instance
        self.descriptor = descriptor
        self.translated_descriptor = getattr(
            descriptor.related.model,
            descriptor.related.field.from_field
        )
        self.storage = storage if storage else RelationStorage()

        self._resolve_initial()

    def _resolve_initial(self):
        """Resolves initial cached value.

        On language controller initialization there could be cached value
        stored in a translated field. Saves it to storage, to avoid extra
        querying.
        """
        self.code = None

        if self.translated_descriptor.is_cached(self.instance):
            cached = self.translated_descriptor.related.get_cached_value(
                self.instance
            )

            if is_translation(cached):
                self.storage.set(cached, cached.language)

    def resolve(self, language: str) -> Optional[models.Model]:
        """Resolves translation for given language from database."""
        # TODO: Add ability to check generic translations relation for
        # cached entities to resolve from.
        instance = self.instance
        descriptor = self.translated_descriptor

        filter_args = descriptor.related.field.get_forward_related_filter(
            instance
        )
        try:
            return (
                descriptor
                .get_queryset(instance=instance, language=language)
                .get(**filter_args)
            )
        except descriptor.related.related_model.DoesNotExist:
            rel_obj = None

        return rel_obj

    def resolve_stored(self, language: str) -> models.Model:
        """Tries to resolve translation for given language from storage.
        If fails - gets it from database.
        """
        return self.storage.get_or_resolve(
            self.instance.pk, language,
            resolver=lambda l: self.resolve(language) or self.instance
        )

    def _set(self, translation: models.Model, language: str):
        setattr(
            self.instance,
            self.descriptor.related.field.from_field,
            translation
        )
        self.code = language

    def inject(self, language: Optional[str] = None):
        """Injects translation for given language into an instance
        `translated` field.

        Args:
            language (str, optional): Language to inject.
                If nothing passes - will get currently available language.
                Defaults to None.
        """
        language = language if language is not None else self.get_language()

        self._set(self.resolve_stored(language), language)

    def __str__(self):
        return self.code or ''

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other

        return super().__eq__(other)


class LanguageControlDescriptor:
    controller_class: Type[LanguageController] = LanguageController
    related: OneToOneRel

    def __init__(self, related):
        self.related = related

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        try:
            return self.related.get_cached_value(instance)
        except KeyError:
            related_pk = instance.pk

            if related_pk is None:
                raise UnsavedLanguageControlAttempt(
                    'Can\'t control translations using language switcher '
                    f'within unsaved {type(instance)} instance.'
                )

        rel_obj = self.controller_class(instance, descriptor=self)
        self.related.set_cached_value(instance, rel_obj)

        return rel_obj

    def __set__(self, instance, value):
        raise ValueError('Can\'t set anything here.')


class LanguageControlField(OnlyRelationMixin, models.OneToOneField):
    related_accessor_class = LanguageControlDescriptor


def apply_magic_to_translation_model(
    model: models.Model,
    parent_model: models.Model,
    entity_field: str = MAGIC_TRANSLATION_ENTITY_FIELD,
    stored_field: str = MAGIC_TRANSLATION_STORED_FIELD,
    control_field: str = MAGIC_TRANSLATION_CONTROL_FIELD,
):
    return type(model.__name__ + 'Magical', (model,), {
        '__module__': model.__module__,
        'Meta': type('Meta', (), {
            'abstract': True,
        }),

        'internal_translation_storage_relation_field': TranslatedRelationField(
            parent_model, on_delete=models.CASCADE, related_name=stored_field,
            from_field=entity_field
        ),
        'internal_translation_control_relation_field': LanguageControlField(
            parent_model, on_delete=models.CASCADE, related_name=control_field,
            from_field=stored_field
        )
    })
