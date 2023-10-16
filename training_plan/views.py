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
            # Create Marathon plan
            user_plan = plan_algo.NewMarathonPlan(user)
            print(user_plan)
            return render(request, "training_plan/plan.html", {
                "user_plan": user_plan
            })
        else:
            # Errors here
            return HttpResponseRedirect(reverse("index"))

    else:
        form = MergedSignUpForm()

    return render(request, "training_plan/register.html", {
        "form": form
    })



