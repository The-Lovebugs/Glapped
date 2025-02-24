from django.apps import AppConfig

class GlappedMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Glapped_main'

    def ready(self):
        import register.signals
