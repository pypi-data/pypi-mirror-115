from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    """
    Config for django_inline_sass application.
    """
    name = 'django_inline_sass'
    label = 'django-inline-sass'
    verbose_name = _('Django Inline SASS')

    def ready(self):
        from django_inline_sass.signals import connect_signals
        connect_signals()
