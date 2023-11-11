import json
from django.core import serializers
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .utils import plan_algo, strava_funcs
from .models import RunnerUser, MarathonPlan, ScheduledRun, CompletedRun, StravaUserProfile
from .forms import MergedSignUpForm

@login_required
def remove_strava_account(request):
    if request.user.is_authenticated:
        username = request.user.username
        strava_funcs.unlink_strava(username)

    return HttpResponseRedirect(reverse("settings"))

@login_required
def settings(request):
    strava_user = None

    if request.user.is_authenticated:
        username = request.user.username
        try:
            user = RunnerUser.objects.get(username=username)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse("index"))
        else:
            try:
                strava_user = StravaUserProfile.objects.get(user=user)
            except Exception as e:
                print(e)

            return render(request, "training_plan/settings.html", {
                "strava_user": strava_user
            })
    else:
        return HttpResponseRedirect(reverse("settings"))

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
                today = date.today() #+ timedelta(days = 344)
                days_to_go = (marathon_plan.end_date - today).days

                # Send user to create a new plan
                if days_to_go <= -1:
                    pass
                    # TODO - return render a template to the user to get them to create a new plan

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
            all_scheduled_runs = list(ScheduledRun.objects.filter(marathon_plan=marathon_plan, date__gt=date.today()).order_by("date").values())
            
        except ScheduledRun.DoesNotExist:
            all_scheduled_runs = None

    return JsonResponse({"all_scheduled_runs": all_scheduled_runs})

@login_required
@require_POST
@csrf_protect
def update_completed_run(request):

    try:
        data = json.loads(request.body)
        payload = data.get("payload") # payload is run_id, date, distance, duration, avg_pace

        if request.user.is_authenticated:
            username = request.user.username
            user = RunnerUser.objects.get(username=username)

            stats_dict = payload.copy()

            # Converting the pace into the correct format for the model
            pace_parts = payload["pace"].split(":")
            formatted_avg_pace = timedelta(minutes=int(pace_parts[0]), seconds=int(pace_parts[1]))


            stats_dict["date"] = datetime.strptime(payload["date"], "%Y-%m-%d")
            stats_dict["distance"] = int(payload["distance"])
            stats_dict["duration"] = int(payload["duration"])
            stats_dict["pace"] = formatted_avg_pace
            run_id_val = stats_dict.pop("run_id")

            # Changing pace to avg_pace like in the model
            stats_dict["avg_pace"] = stats_dict["pace"]
            stats_dict.pop("pace")
            
            scheduled_run = ScheduledRun.objects.get(id=payload["run_id"])

            # Check first if there isn"t a completed run, if so make one, if not then update the values
            completed_run, created = CompletedRun.objects.get_or_create(scheduled_run=scheduled_run, defaults=stats_dict) # Get the actual plan from the query set
            
            if not created:  # Use "get" to get the CompletedRun
                for field in stats_dict:
                    setattr(completed_run, field, stats_dict[field])
                completed_run.save()

            # Add back run_id before response
            stats_dict["run_id"] = run_id_val
            return JsonResponse({"message": "Stats for run updated successfully", "payload": stats_dict})
        else:
            return JsonResponse({"error": "User is not logged in"}, status=403)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def get_todays_run(request):

    if request.user.is_authenticated:
        today = date.today() #+ timedelta(days = 339)

        username = request.user.username
        user = RunnerUser.objects.get(username=username)
        marathon_plan = MarathonPlan.objects.get(user=user) 

        scheduled_run = ScheduledRun.objects.get(marathon_plan=marathon_plan, date=today)

        try:
            todays_run = CompletedRun.objects.get(date=today, scheduled_run=scheduled_run)
            completed = True
        except CompletedRun.DoesNotExist:
            todays_run = scheduled_run
            completed = False

        try:
            serialized_data = serializers.serialize("python", [todays_run])

            response_data = serialized_data[0]["fields"]
            response_data['run_id'] = serialized_data[0]['pk'] # Add 'run_id' to the response_data dictionary
            response_data['completed'] = completed # Add completed to easily identify if working with the scheduled or completed run

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else: 
        return HttpResponseRedirect(reverse("index")) 

@login_required
def get_strava_run(request):

    if request.user.is_authenticated:

        username = request.user.username
        user = RunnerUser.objects.get(username=username)
        marathon_plan = MarathonPlan.objects.get(user=user) 
        strava_funcs.refresh_trava_token(username)
        todays_run = ScheduledRun.objects.get(marathon_plan=marathon_plan, date=date.today())

        try:
            completed_run = CompletedRun.objects.get(scheduled_run=todays_run)
        except Exception as e:
            completed_run = None
            print(e)
        try:
            if not completed_run:
                strava_funcs.get_strava_run_func(user, todays_run)

        except LookupError:
            return HttpResponseRedirect(reverse("index")) 

    return HttpResponseRedirect(reverse("index")) 

