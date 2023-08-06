from django.contrib import admin


__all__ = 'TranslationsInlineAdmin',


class TranslationsInlineAdmin(admin.StackedInline):
    extra = 0
