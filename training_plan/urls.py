from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scheduled-runs", views.scheduled_runs, name="scheduled-runs"),
    path("accounts/register", views.register, name="register"),
    path("api/get-scheduled-runs", views.get_scheduled_runs, name="get-scheduled-runs")
]
