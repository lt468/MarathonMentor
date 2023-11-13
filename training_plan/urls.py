"""
Django URL patterns for the MarathonMentor training plan app.

This module defines URL patterns for various views in the MarathonMentor training plan app.

URL Patterns:
- /: The index view, displaying the home page.
- /scheduled-runs: Displays scheduled runs for the user.
- /completed-runs: Displays completed runs for the user.
- /settings: Displays user settings.
- /accounts/register: Handles user registration.
- /social/remove-strava-account: Removes the Strava account linked to the user.
- /api/get-scheduled-runs: API endpoint to get scheduled runs for the user.
- /api/get-completed-runs: API endpoint to get completed runs for the user.
- /api/get-todays-run: API endpoint to get today's scheduled run for the user.
- /api/update-completed-run: API endpoint to update a completed run.

Usage:
1. Include these URL patterns in your Django project's main urls.py using the include function:
   python
   from django.urls import include, path

   urlpatterns = [
       # ... other URL patterns ...
       path('training_plan/', include('training_plan.urls')),
       # ... other URL patterns ...
   ]

    Access the views by navigating to the corresponding URLs.

Example:

# In the main urls.py of your Django project
from django.urls import include, path

urlpatterns = [
    # ... other URL patterns ...
    path('training_plan/', include('training_plan.urls')),
    # ... other URL patterns ...
]

This example assumes that the training_plan.urls module contains the URL patterns defined in this file.
"""

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
