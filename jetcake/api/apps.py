from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class APIConfig(AppConfig):
    name = "jetcake.api"
    verbose_name = _("API")

    def ready(self):
        try:
            import jetcake.users.signals  # noqa F401
        except ImportError:
            pass
