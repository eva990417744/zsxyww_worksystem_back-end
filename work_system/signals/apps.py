from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SignalsConfig(AppConfig):
    name = 'work_system.signals'
    verbose_name = _('signals')

    def ready(self):
        import work_system.signals.signals