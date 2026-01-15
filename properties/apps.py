from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        """
        Import signal handlers when the app is ready.

        This method is called when Django starts and all models are loaded.
        We import signals here to register the signal handlers with Django's
        signal dispatcher.
        """
        import properties.signals  # noqa: F401
