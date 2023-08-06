from dataclasses import dataclass, field
from typing import Dict, Sequence, Tuple
from django.conf import settings as django_settings
from px_settings.contrib.django import settings as s

from .types import FallbackLanguages


__all__ = 'Settings', 'settings'


@s('PXD_LINGUA')
@dataclass
class Settings:
    # FIXME: Naming should be changed, or at least revised.
    LANGUAGES: Sequence[str] = field(
        default_factory=lambda: [key for key, _ in django_settings.LANGUAGES]
    )
    FALLBACK_LANGUAGES: FallbackLanguages = field(default_factory=lambda: {})
    DEFAULT_LANGUAGE: str = field(
        default_factory=lambda: django_settings.LANGUAGE_CODE
    )


settings = Settings()

# FIXME: Something wrong happening by default. Should be able to enable check here.
# assert settings.DEFAULT_LANGUAGE in settings.LANGUAGES, (
#     'Default language not in LANGUAGES setting.'
# )
