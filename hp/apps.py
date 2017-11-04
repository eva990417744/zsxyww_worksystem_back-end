from django.apps import AppConfig


class HpConfig(AppConfig):
    name = 'hp'

    def ready(self):
        import hp.signals
