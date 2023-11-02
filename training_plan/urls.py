from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scheduled-runs", views.scheduled_runs, name="scheduled-runs"),
    path("settings", views.settings, name="settings"),
    path("accounts/register", views.register, name="register"),
    path("oauth/complete/strava/", views.strava_oauth_callback, name="strava_oauth_callback"),
    path("api/get-scheduled-runs", views.get_scheduled_runs, name="get-scheduled-runs"),
]
