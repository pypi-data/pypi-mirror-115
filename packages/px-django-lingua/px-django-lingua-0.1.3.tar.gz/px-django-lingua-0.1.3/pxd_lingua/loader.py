from typing import Callable, Dict, Optional, Tuple, Generic, TypeVar, Union
from django.db import models

from .utils import LanguageGetterMixin, is_translation


__all__ = 'RelationStorage',

T = TypeVar('T', bound=models.Model)
E = TypeVar('E', bound=models.Model)


class RelationStorage(Generic[E, T]):
    storage: Dict[Tuple[int, str], Union[E, T]]

    def __init__(self):
        self.storage = {}

    def get(self, entity_id: int, language: str) -> Optional[Union[E, T]]:
        key = entity_id, language

        return self.storage.get(key, None)

    def set(self, translated: Union[E, T], language: str):
        if not is_translation(translated):
            # It's not a translated entity, it's an entity itself
            self.storage[(translated.pk, language)] = translated

            return

        self.storage[(translated.entity_id, translated.language)] = translated
        self.storage[(translated.entity_id, language)] = translated

    def get_or_resolve(
        self,
        entity_id: int,
        language: str,
        resolver: Callable
    ) -> Union[E, T]:
        """Tries to resolve translation for given language from storage.
        If fails - gets it from resolver.
        """
        translation = self.get(entity_id, language)

        if translation is not None:
            return translation

        translation = resolver(language)
        self.set(translation, language)

        return translation
