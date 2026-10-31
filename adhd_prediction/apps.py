from django.apps import AppConfig


class AdhdPredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adhd_prediction'

    def ready(self):
        import adhd_prediction.signals
