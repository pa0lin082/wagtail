from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from wagtail.wagtailimages import get_image_model_string

from . import checks  # NOQA


class WagtailImagesAppConfig(AppConfig):
    name = 'wagtail.wagtailimages'
    label = 'wagtailimages'
    verbose_name = "Wagtail images"

    def get_models(self, include_auto_created=False, include_swapped=False):
        """
        Returns an iterable of models except ['Image', 'Rendition']
        when User customize WAGTAILIMAGES_IMAGE_MODEL

        By default, the following models aren't included:

        - auto-created models for many-to-many relations without
          an explicit intermediate table,
        - models that have been swapped out.

        Set the corresponding keyword argument to True to include such models.
        Keyword arguments aren't documented; they're a private API.
        """
        self.apps.check_models_ready()
        for model in self.models.values():
            if get_image_model_string() != 'wagtailimages.Image' \
                and model.__name__ in ['Image', 'Rendition']:
                continue
            if model._meta.auto_created and not include_auto_created:
                continue
            if model._meta.swapped and not include_swapped:
                continue
            yield model

    def ready(self):
        from wagtail.wagtailimages.signal_handlers import register_signal_handlers
        register_signal_handlers()
