"""
Django admin configuration for the Training Plan app.

This module registers models from the Training Plan app with the Django admin site, allowing administrators to manage the data through the admin interface.

Models Registered:
- RunnerUser: Custom user model representing runners.
- MarathonPlan: Model for storing marathon training plans.
- CompletedRun: Model for recording completed runs.
- ScheduledRun: Model for storing scheduled runs in training plans.
- StravaUserProfile: Model for storing Strava user profile information.

Usage:
- Visit the Django admin site to manage RunnerUser, MarathonPlan, CompletedRun, ScheduledRun, and StravaUserProfile models.

Example:
    To view and manage the RunnerUser model:
    
    from django.contrib import admin
    from .models import RunnerUser, MarathonPlan, ScheduledRun, CompletedRun, StravaUserProfile

    admin.site.register(RunnerUser)
    admin.site.register(MarathonPlan)
    admin.site.register(CompletedRun)
    admin.site.register(ScheduledRun)
    admin.site.register(StravaUserProfile)
    

Note: Ensure that the models are appropriately defined in the 'models.py' file before registering them here.
"""

from django.contrib import admin
from .models import RunnerUser, MarathonPlan, ScheduledRun, CompletedRun, StravaUserProfile

# Register your models here.
admin.site.register(RunnerUser)
admin.site.register(MarathonPlan)
admin.site.register(CompletedRun)
admin.site.register(ScheduledRun)
admin.site.register(StravaUserProfile)
