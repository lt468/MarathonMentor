from django.apps import AppConfig

class TrainingPlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_plan'

    def ready(self):
        # Ensure the templatetags directory is loaded
        try:
            import training_plan.templatetags
        except ImportError:
            pass
