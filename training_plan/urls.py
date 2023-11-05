from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scheduled-runs", views.scheduled_runs, name="scheduled-runs"),
    path("settings", views.settings, name="settings"),
    path("mark-as-complete", views.mark_as_complete, name="mark-as-complete"),
    path("accounts/register", views.register, name="register"),
    path("api/get-scheduled-runs", views.get_scheduled_runs, name="get-scheduled-runs"),
]
