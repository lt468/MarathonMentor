from django.contrib import admin
from .models import RunnerUser, Run, MarathonPlan, ScheduledRun, TrainingWeek

# Register your models here.
admin.site.register(RunnerUser)
admin.site.register(Run)
admin.site.register(MarathonPlan)
admin.site.register(ScheduledRun)
admin.site.register(TrainingWeek)
