from typing import Dict, Optional, Sequence
from django.db import models
from django.utils.translation import pgettext_lazy, pgettext

from .query import TranslationQuerySet
from .utils import get_language_choices
from .conf import settings


__all__ = (
    'TRANSLATION_POSTFIX',
    'TRANSLATION_RELATED_NAME',
    'translated_model_uniques',
    'create_translated_model',
)

EMPTY = object()
TRANSLATION_POSTFIX: str = 'Translation'
TRANSLATION_RELATED_NAME: str = 'translations'


def translated_model_uniques():
    return (
        ('language', 'entity_id'),
    )


def collect_model_fields(model: models.Model, fields: Sequence[str]) -> Dict[str, models.Field]:
    return {
        field: model._meta.get_field(field).clone()
        for field in fields
    }


def create_translated_model(
    model: models.Model,
    fields: Optional[Sequence[str]] = None,
    postfix: str = TRANSLATION_POSTFIX,
    default_language: Optional[str] = EMPTY,
    languages: Optional[Sequence] = EMPTY,
    related_name: str = TRANSLATION_RELATED_NAME,
    verbose_name: Optional[str] = None,
    verbose_name_plural: Optional[str] = None,
    abstract: bool = False
) -> models.Model:
    base_name = model.__name__
    name = base_name + postfix
    no_fields = fields is None or len(fields) == 0

    assert not (not abstract and no_fields), (
        'Provide at least one field in `fields` or made model an abstract.'
    )

    Meta = type('Meta', (), {
        key: value
        for key, value in (
            ('verbose_name', verbose_name),
            ('verbose_name_plural', verbose_name_plural),
            ('abstract', abstract),
            ('unique_together', translated_model_uniques()),
        )
        if value
    })

    class TranslatedModel(models.Model):
        objects = TranslationQuerySet.as_manager()

        class Meta:
            abstract = True

        id = models.BigAutoField(
            primary_key=True, verbose_name=pgettext_lazy('pxd_lingua', 'ID')
        )
        language = models.CharField(
            verbose_name=pgettext_lazy('pxd_lingua', 'Language'),
            max_length=32, choices=(
                get_language_choices()
                if languages is EMPTY
                else languages
            ),
            default=(
                settings.DEFAULT_LANGUAGE
                if default_language is EMPTY
                else default_language
            ),
            null=False, blank=False,
        )
        entity = models.ForeignKey(
            model,
            verbose_name=pgettext_lazy('pxd_lingua', 'Translation entity'),
            null=False, blank=False, on_delete=models.CASCADE,
            related_name=related_name
        )

        def __str__(self):
            return (
                pgettext(
                    'pxd_lingua',
                    '"{language}" translation for #{entity_id} entity'
                )
                .format(language=self.language, entity_id=self.entity_id)
            )

    return type(name, (TranslatedModel,), {
        **({} if no_fields else collect_model_fields(model, fields)),
        '__module__': model.__module__,
        'Meta': Meta,
    })
