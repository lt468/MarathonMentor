from django.contrib.auth import authenticate, login
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
            return render(request, "registration/register.html", {
                "data": 5
            })

    return render(request, "training_plan/index.html", {
        "data": 5
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
