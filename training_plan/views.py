from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .utils import plan_algo
from .models import RunnerUser
from .forms import MergedSignUpForm

def index(request):
    # Check the Marathon date is valid
    if request.user.is_authenticated:
        username = request.user.username

        # Verify that the username leads to a valid user
        try:
            user = RunnerUser.objects.get(username=username)

        except RunnerUser.DoesNotExist:
            raise ValueError("User doesn't exist (likely not logged in or incorrect username passed)")
    else:
        # TODO - return a redirect if user isn't logged in
        user = None

    return render(request, "training_plan/index.html", {
        "data": 5
    })

def register(request):

    if request.method == "POST":
        form = MergedSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Marathon plan object
            plan = plan_algo.NewMarathonPlan(user)

            # Create new plan
            success, user_plan = plan.create_plan()
            print(success)

            # If there is an error in the marathon date
            if not success:
                return render(request, "trainin_plan/error.html", {
                    "error_msg": user_plan
                }, status=422)

            # Schedule the runs
            plan.create_runs_in_plan()

            return render(request, "training_plan/plan.html", {
                "user_plan": user_plan
            })
        else:
            # Errors here
            print(form.errors)
            return render(request, "training_plan/error.html", {
                "error_msg": "something went wrong with user sign-up"
            })

    else:
        form = MergedSignUpForm()

    return render(request, "training_plan/register.html", {
        "form": form
    })



