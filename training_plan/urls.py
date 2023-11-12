from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scheduled-runs", views.scheduled_runs, name="scheduled-runs"),
    path("completed-runs", views.completed_runs, name="completed-runs"),
    path("settings", views.settings, name="settings"),
    path("accounts/register", views.register, name="register"),
    path("social/remove-strava-account",
         views.remove_strava_account, name="remove-strava-account"),
    path("api/get-scheduled-runs", views.get_scheduled_runs,
         name="get-scheduled-runs"),
    path("api/get-completed-runs", views.get_completed_runs,
         name="get-completed-runs"),
    path("api/get-todays-run", views.get_todays_run, name="get-todays-run"),
    path("api/update-completed-run", views.update_completed_run,
         name="update-completed-run")
]
