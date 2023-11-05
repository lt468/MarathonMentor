from urllib.parse import parse_qs, urlparse
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from social_django.utils import psa

from .utils import plan_algo
from .models import RunnerUser, MarathonPlan, ScheduledRun, StravaUserProfile
from .forms import MergedSignUpForm, CompletedRunForm

@login_required
def mark_as_complete(request):
    if request.method == "POST":
        form = CompletedRunForm(request.POST, request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index")) # For now, change in a bit
        else:
            # Errors here
            print(form.errors)
            return render(request, "training_plan/mark_as_complete.html", {
                "form": form
            })
    else:
        form = CompletedRunForm(request.user)

    return render(request, "training_plan/mark_as_complete.html", {
        "form": form
    })

@login_required
def settings(request):
    return render(request, "training_plan/settings.html")

@login_required
def scheduled_runs(request):
    return render(request, "training_plan/scheduled_runs.html")

def index(request):
    marathon_plan = days_to_go = todays_run = next_runs = today = None

    if request.user.is_authenticated:
        username = request.user.username

        try:
            user = RunnerUser.objects.get(username=username)
            marathon_plan = MarathonPlan.objects.get(user=user) # Get the actual plan from the query set
            if marathon_plan:
                # Calculate the days until the marathon
                today = date.today()
                days_to_go = (marathon_plan.end_date - today).days

                try:
                    todays_run = ScheduledRun.objects.get(marathon_plan=marathon_plan, date=today)
                except ScheduledRun.DoesNotExist:
                    # If there is no run scheduled then it means that the plan hasn't started yet
                    todays_run = None

                try:
                    next_runs = ScheduledRun.objects.filter(marathon_plan=marathon_plan, date__gte=today).order_by('date')[1:4]
                except IndexError:
                    # If there is no run scheduled then it means that the plan hasn't started yet
                    next_runs = None

            else:
                # No marathon plan found for the specified user
                print(f"No marathon plan found for user {username}")

        except RunnerUser.DoesNotExist:
            # User with the specified username does not exist
            print(f"User with username {username} does not exist.")

    return render(request, "training_plan/index.html", {
        "plan": marathon_plan,
        "today": today,
        "days_to_go": days_to_go,
        "todays_run": todays_run,
        "next_runs": next_runs,
        "greeting": calc_greeting() 
    })


def register(request):
    if request.method == "POST":
        form = MergedSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            plan = plan_algo.NewMarathonPlan(user) # Create Marathon plan object

            # Create new plan
            success, user_plan = plan.create_plan()

            # If there is an error in the marathon date
            if not success:
                return render(request, "trainin_plan/error.html", {
                    "error_msg": user_plan
                }, status=422)

            # Schedule the runs
            plan.create_runs_in_plan()

            # To log the user in after registration
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)       

            return HttpResponseRedirect(reverse("index"))
        else:
            # Errors here
            print(form.errors)
            return render(request, "registration/register.html", {
                "form": form
            })
    else:
        form = MergedSignUpForm()

    return render(request, "registration/register.html", {
        "form": form
    })

""" Helper functions """
def calc_greeting():
    hours = datetime.now().hour

    if hours >= 4 and hours < 12:
        time_of_day = "morning"
    elif hours >= 12 and hours < 17:
        time_of_day = "afternoon"
    elif hours >= 17 and hours < 23:
        time_of_day = "evening"
    else:
        time_of_day = "night"

    return time_of_day

@login_required
def get_scheduled_runs(request):
    username = request.user.username

    user = RunnerUser.objects.get(username=username)
    marathon_plan = MarathonPlan.objects.get(user=user) 
    all_scheduled_runs = None
    if marathon_plan:

        try:
            all_scheduled_runs = list(ScheduledRun.objects.filter(marathon_plan=marathon_plan, date__gt=date.today()).order_by('date').values())
            
        except ScheduledRun.DoesNotExist:
            all_scheduled_runs = None

    return JsonResponse({'all_scheduled_runs': all_scheduled_runs})





