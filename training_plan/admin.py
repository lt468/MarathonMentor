from django.contrib import admin
from .models import RunnerUser, MarathonPlan, ScheduledRun, CompletedRun, StravaUserProfile

# Register your models here.
admin.site.register(RunnerUser)
admin.site.register(MarathonPlan)
admin.site.register(CompletedRun)
admin.site.register(ScheduledRun)
admin.site.register(StravaUserProfile)
