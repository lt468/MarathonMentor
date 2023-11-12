import requests
from datetime import datetime, timedelta, date
from django.utils import timezone
import urllib3
from ..models import StravaUserProfile, RunnerUser, CompletedRun
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from decouple import config

def save_profile(user, response, *args, **kwargs):

    client_id = response["athlete"]["id"]
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    expires_at = response["expires_at"]

    # Linking the Strava account to the runneruser
    strava_profile = StravaUserProfile(
        user = user,
        client_id = client_id,
        strava_access_token = access_token,
        strava_refresh_token = refresh_token,
        expires_at = datetime.fromtimestamp(expires_at)
    )

    strava_profile.save()

def get_strava_run_func(user, todays_run):

    try:
        strava_profile = StravaUserProfile.objects.get(user=user)
    except StravaUserProfile.DoesNotExist:
        raise LookupError("Strava profile not found")
    else:
        # URLs
        activites_url = "https://www.strava.com/api/v3/athlete/activities"

        access_token = strava_profile.strava_access_token

        # Get the latest n activities
        n = 5
        header = {'Authorization': 'Bearer ' + access_token} # Need to use the access token for the user you want to get the runs on 
        param = {'per_page': n, 'page': 1}
        my_dataset = requests.get(activites_url, headers=header, params=param).json()

        # Get the latest run activity of today's run
        for activity in my_dataset: 
            date_of_run = activity["start_date"].split("T")[0]
            date_of_run_formatted = (datetime.strptime(date_of_run,'%Y-%m-%d')).date()

            if (activity["type"] == "Run") and (date_of_run_formatted == date.today()):

                distance = int(activity["distance"] // 1000)
                duration = int(activity["moving_time"] // 60)
                # Calculate pace in seconds per kilometer
                pace_seconds_per_m = activity["moving_time"] / activity["distance"]
                # Convert pace back to minutes and seconds
                pace_minutes, pace_seconds = divmod(pace_seconds_per_m * 1000, 60)
                # Format the result as mm:ss
                avg_pace = timedelta(minutes=pace_minutes, seconds=pace_seconds)

                completed_run = CompletedRun(
                    scheduled_run=todays_run,
                    date=date_of_run_formatted,
                    distance=distance,
                    duration=duration,
                    avg_pace=avg_pace
                )
                completed_run.save()
                break

def unlink_strava(username):
    try:
        user = RunnerUser.objects.get(username=username)
        strava_profile = StravaUserProfile.objects.get(user=user)
        if strava_profile:
            strava_profile.delete()

    except Exception as e:
        print(f"No user account found: {e}")

def refresh_trava_token(username):
    try:
        user = RunnerUser.objects.get(username=username)
        strava_profile = StravaUserProfile.objects.get(user=user)
    except Exception as e:
        raise LookupError("Strava profile not found", e)
    else:

        # Your Strava API credentials
        client_id = config("STRAVA_CLIENT_ID")
        client_secret = config("STRAVA_CLIENT_SECRET")

        # Check if the access token has expired
        if strava_profile.expires_at <= timezone.now():
            # Access token has expired, refresh it using the refresh token
            refresh_token = strava_profile.strava_refresh_token
            token_url = 'https://www.strava.com/oauth/token'

            # Prepare the data for the POST request
            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }

            # Make the POST request to refresh the token
            response = requests.post(token_url, data=data)

            if response.status_code == 200:
                # Update the model with the new access token and refresh token
                token_data = response.json()
                strava_profile.strava_access_token = token_data['access_token']
                strava_profile.strava_refresh_token = token_data['refresh_token']
                expires_in = token_data['expires_in']
                strava_profile.expires_at = timezone.now() + timedelta(seconds=expires_in)
                strava_profile.save()
            else:
                # Handle the error, e.g., log it or raise an exception
                print(f"Token refresh failed with status code {response.status_code}")
        else:
            # Access token is still valid, no need to refresh
            print("Strava access token still valid")
            
