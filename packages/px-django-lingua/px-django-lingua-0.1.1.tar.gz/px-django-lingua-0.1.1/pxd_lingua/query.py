from typing import Optional, Sequence, TypeVar
from itertools import chain

from django.db import models

from .utils import get_fallback_languages


__all__ = (
    'filter_by_field_in_order',

    'TranslationQuerySet',
)

T = TypeVar('T')


def filter_by_field_in_order(
    query: T,
    field_lookup: str,
    values: Sequence,
    distinct: Sequence[str],
    annotation_name: str = '_field_order_rank',
    order_by: Sequence[str] = [],
) -> T:
    amount = len(values)

    if amount == 0:
        return query

    if amount == 1:
        return query.filter(**{field_lookup: values[0]})

    whens = [
        models.When(language=language, then=i)
        for i, language in enumerate(values)
    ]
    order_by = chain(distinct, (annotation_name,), order_by)

    query = (
        query
        .filter(**{f'{field_lookup}__in': values})
        .annotate(**{annotation_name: models.Case(
            *whens, default=amount, output_field=models.IntegerField()
        )})
        .order_by(*order_by)
        .distinct(*distinct)
    )

    return query


class TranslationQuerySet(models.QuerySet):
    def by_language_order(
        self: T,
        *languages: Sequence[str],
    ) -> T:
        return filter_by_field_in_order(
            self,
            'language',
            languages,
            ('entity_id',),
            annotation_name='_languages_rank',
            order_by=self.query.order_by
        )

    def by_language(self: T, language: Optional[str] = None) -> T:
        # TODO: Make fallback_languages parameter configurable per
        # queryset instance.
        language, fallbacks = get_fallback_languages(language)

        return self.by_language_order([language] + fallbacks)
