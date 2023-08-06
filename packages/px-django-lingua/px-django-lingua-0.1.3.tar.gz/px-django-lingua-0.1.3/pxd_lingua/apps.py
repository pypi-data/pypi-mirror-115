from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('LinguaConfig',)


class LinguaConfig(AppConfig):
    name = 'pxd_lingua'
    verbose_name = pgettext_lazy('pxd_lingua', 'Lingua')
