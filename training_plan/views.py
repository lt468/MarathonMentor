from django.shortcuts import render
from .utils import plan_algo
from .models import RunnerUser, MarathonPlan

def index(request):
    # Check the Marathon date is valid
    if request.user.is_authenticated:
        username = request.user.username

        # Verify that the username leads to a valid user
        try:
            user = RunnerUser.objects.get(username=username)

        except RunnerUser.DoesNotExist:
            raise ValueError("User doesn't exist (likely not logged in or incorrect username passed)")

        plan_algo.CreatePlan(user) # Create the phases in the plan

        plan = MarathonPlan.objects.all()
        plan_algo.CreateRunsInPlan(user)

    else:
        # TODO - return a redirect if user isn't logged in
        user = None

    return render(request, "training_plan/index.html", {
        "data": plan
    })
