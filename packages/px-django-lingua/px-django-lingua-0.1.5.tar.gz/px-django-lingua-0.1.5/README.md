# Lingua

Simple translations implementation for django models.

## Installation

```sh
pip install px-django-lingua
```

In `settings.py`:

```python
PXD_LINGUA = {
  # By default uses django's LANGUAGE_CODE.
  'DEFAULT_LANGUAGE': 'en',
  # By default uses django's LANGUAGES to get list of available languages.
  'LANGUAGES': ('en', 'fr', 'de', 'ru'),
  # For each registered language code could be a default language fallbacks:
  'FALLBACK_LANGUAGES': {
    'en': ('fr',),
    'ru': ('en',),
    'de': ('en', 'fr',),
    # There could be any number of languages.
    # The order in which they are specified - is the order in which they
    # will be resolved if there's no translation with previous language found.
    'fr': ('en', 'ru', 'de',)
  },
}
```

## Usage

### Translation generation

Unlike `django-parler` "raw" model fields will not be removed.

```python
from django.db import models

from pxd_lingua import create_translation_model


class Content(models.Model):
  title = models.CharField(max_length=40)
  content = models.TextField()


# Factory will generate new model with identical fields.
ContentAlternateTranslation = create_translation_model(
  Content, fields=('title', 'content'),
)
# Or.
# New model can be fully customized if you wish so:
ContentAlternateTranslation = create_translation_model(
  Content,
  # List of fields. Can be empty only when an abstract model creates(maybe
  # you need some very custom translation behavior).
  fields=('title', 'content'),
  # Model name postfix.
  postfix='AlternateTranslation',
  # By default is uses default language from PXD_LINGUA settings.
  default_language='en',
  # Available languages can also be changed for a particular model.
  # By default - uses languages from settings.
  languages=(
    ('en', _('English')),
  ),
  # Entity foreign relation name.
  # Bu default: 'translations', but can be anything.
  related_name='translations',
  # Related name for a "magic" field that stores current translation entity.
  stored_related_name='translated',
  # Related name for a language "magic" switch controller.
  language_control_related_name='language',
  # Model's verbose name.
  verbose_name=None,
  # Model's plural verbose name.
  verbose_name_plural=None,
  # Boolean, to whether create abstract or "true" model. False by default.
  abstract=False,
  # Boolean. Disables/enables magic methods for translatable model instances.
  with_magic=True,
)
```

Resulting database schema will be something like:

<p align="center"><img src="https://i.postimg.cc/tTCQQxN6/db-example.png" alt="Translated db schema" /></p>

### Querying

Simple querying:

```python
from .models import Content, ContentAlternateTranslation


# Getting translations for a list of items:
translations = (
  ContentAlternateTranslation.objects
  .filter(entity_id__in=(1, 2, 3, 4, 5))
  # This method will get only translations that are either in English or
  # in French if there is no english version available.
  # There could be any number of languages passed here.
  # At most one translation instance per entity will be returned, because
  # there could be no entity translations for some entity at all.
  .by_language_order('en', 'fr')
)

# To "enable" internal fallback mechanics use `by_language`:
translations = (
  ContentAlternateTranslation.objects
  .filter(entity_id__in=(1, 2, 3, 4, 5))
  # For a more simple usecase when code executes inside a django context
  .by_language('en')
  # For a more simple usecase when code executes inside a django context
  # and you need a translations for current user language `language` parameter
  # may be omitted:
  .by_language()
)

# Content's related manager also do have those methods:
obj = Content.objects.get(pk=1)
translation = obj.translations.by_language_order('fr', 'en').first()
# Or
translation = obj.translations.by_language('fr').first()
```

### Admin

Just use a regular inliner for admin panel:

```python
from django.contrib import admin
from pxd_lingua.admin import TranslationsInlineAdmin

from .models import Content, ContentTranslation


class ContentTranslationInlineAdmin(TranslationsInlineAdmin):
  model = ContentTranslation


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
  list_display = 'title', 'content',
  inlines = ContentTranslationInlineAdmin,
```

It might be a little bit messy, when there will be a lot of languages. But instead it's simple and all django admin "themes" supports them.

You may also register model separately if you wish, of course.

### Magic

A **ROAD TO HELL** starts here.

Please, try to use magic methods as little as possible. Preparing data before usage is the best option you may end up with. Magic mechanics should be used only in force majeure situations. They are working as expected, but please, **be careful**.

If magic enabled on generation - translatable model will have 2 additional fields:

- `translated`: Storage field, that holds current translation object(translation model instance). It's a fake one-to-one field reverse relation. It doesen't creates one but looks and works similar to that.
- `language`: Controller for language switching. It stores previously injected model instances inside, so there will not be any additional database calls on language switching there and back again.

Both of those fields are added similar to a reverse relation mechanics.

Translations will **never** be "injected" into a source instance. Use `translated` or `translations` for get access to a translations.

Naming conflicts could be easily resolved on model translation generation by changing `stored_related_name` and `language_control_related_name` parameters respectively.

#### Simple get

To get current translation object just access `translated` field.

```python
from django.utils.translation import override

from .models import Content, ContentAlternateTranslation


obj = Content.objects.get(pk=1)
obj.title
# > 'Some title'
obj.content
# > 'Some content'

# If you need a translation instance `translated` field is at your service:
type(obj.translated)
# > <class your_app.models.ContentAlternateTranslation>

# Language of the translation
obj.translated.language
# > 'en'
# `entity` is a foreign relation to a translated object.
obj.translated.entity_id == obj.id
# > True
obj.translated.title
# > 'Some English translated title'
obj.translated.content
# > 'Some English translated content'
```

If there is no translation for provided language found the untranslated object will be inserted as current translation. This is done to **prevent** things like:

```python
title = obj.translated.title if obj.translated is not None else obj.title
```

So there is **always** will be a "translation" - **it is guaranteed**.

```python
# No translation for current language exists:
obj.translated == obj
# > True
obj.translated.title == obj.title
# > True
```

#### Querying

As `translated` field is just a one-to-one reverse relationship it could be easily prefetched using built in `.prefetch_related('translated')` mechanics.

But beware. Prefetch will use current language at a time the query will be executed, not the time queryset created.

```python
with override('de'):
  contents = Content.objects.prefetch_related('translated')

with override('en'):
  # Prefetch will use current language at a time the query will be executed.
  content = contents.first()
  # No additional queries here
  content.translated.language
  # > 'en'

with override('de'):
  content = (
    Content.objects
    .prefetch_related(
      Prefetch(
        'translated',
        # Always use `by_language` or `by_language_order` methods.
        # Or force distinct by `entity_id`, otherwise prefetch
        # will find more than one translation per instance.
        queryset=ContentTranslation.objects.by_language()
      )
    )
  )

with override('en'):
  # But custom prefetch will resolve current language at the time of it's
  # creation.
  content = content.first()
  content.translated.language
  # > 'de'
```

#### Language switch

```python
from django.utils.translation import override

from .models import Content, ContentAlternateTranslation


obj = Content.objects.get(pk=1)

with override('en'):
  # First time when translated will resolve it will get translation for
  # a current language.
  obj.translated.language
  # > 'en'
  obj.translated.entity_id == obj.id
  # > True
  obj.translated.title
  # > 'Some translated title'
  obj.translated.content
  # > 'Some translated content'

with override('fr'):
  # There wouldn't be any updates here.
  # Because translated field will be resolved only once.
  # You must manually inject other language version, if it's required.
  obj.translated.language
  # > 'en'

# To force translation language change you must call language controller
# to inject new language translation.
obj.language.inject('de')
obj.translated.language
# > 'de'

with override('de'):
  # Default language will be used when `inject` is called without language.
  obj.language.inject()
  obj.translated.language
  # > 'de'
```
