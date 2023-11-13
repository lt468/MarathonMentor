"""
This module defines the configuration for the training_plan app.
"""
from django.apps import AppConfig


class TrainingPlanConfig(AppConfig):
    """
    Configuration class for the `training_plan` Django app.

    Attributes:
    - `default_auto_field` (str): The default primary key field type.
    - `name` (str): The name of the app.

    Methods:
    - `ready()`: Method called when the app is ready.
      Ensures that the `templatetags` directory is loaded.

    Example:
    ```
    class TrainingPlanConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'training_plan'

        def ready(self):
            # Ensure the templatetags directory is loaded
            try:
                import training_plan.templatetags
            except ImportError:
                pass
    ```
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_plan'

    def ready(self):
        """
        Method called when the app is ready.
        Ensures that the `templatetags` directory is loaded.
        """
        try:
            import training_plan.templatetags
        except ImportError:
            pass
