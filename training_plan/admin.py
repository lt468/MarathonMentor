from django.contrib import admin
from .models import RunnerUser, Run, MarathonPlan, ScheduledRuns

# Register your models here.
admin.site.register(RunnerUser)
admin.site.register(Run)
admin.site.register(MarathonPlan)
admin.site.register(ScheduledRuns)
