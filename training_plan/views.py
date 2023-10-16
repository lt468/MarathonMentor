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
        else:
            # Errors here
            pass

        # List of register attributes

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        dob = request.POST["dob"]
        weight = request.POST["weight"]
        height = request.POST["height"]
        fitness_level = request.POST["fitness_level"]
        date_of_marathon = request.POST["date_of_marathon"]

        # Ensure password matches confirmation
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        if password !=  confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = RunnerUser.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username,
                password = password,
                email = email,
                dob = dob,
                weight = weight,
                height = height,
                fitness_level = fitness_level,
                date_of_marathon = date_of_marathon
            )
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        # Create Marathon plan
        user_plan = plan_algo.NewMarathonPlan(user)
        print(user_plan)

        return HttpResponseRedirect(reverse("index"))

