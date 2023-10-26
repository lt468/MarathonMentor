from datetime import date
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .utils import plan_algo
from .models import RunnerUser, MarathonPlan, ScheduledRun
from .forms import MergedSignUpForm


def index(request):
    marathon_plan = next_10_runs = days_to_go = None

    if request.user.is_authenticated:
        username = request.user.username

        try:
            user = RunnerUser.objects.get(username=username)
            marathon_plan = MarathonPlan.objects.filter(user=user).first() # Get the actual plan from the query set
            if marathon_plan:
                # Found the marathon plan for the specified user
                print(f"Marathon plan for user {username}: {marathon_plan}")
                # Calculate the days until the marathon
                today = date.today()
                days_to_go = (marathon_plan.end_date - today).days

                # Query for the next 10 runs based on the marathon plan and current date
                next_10_runs = ScheduledRun.objects.filter(marathon_plan=marathon_plan, date__gte=today).order_by('date')[:10]

            else:
                # No marathon plan found for the specified user
                print(f"No marathon plan found for user {username}")

        except RunnerUser.DoesNotExist:
            # User with the specified username does not exist
            print(f"User with username {username} does not exist.")

    return render(request, "training_plan/index.html", {
        "plan": marathon_plan,
        "days_to_go": days_to_go,
        "next_10_runs": next_10_runs
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

