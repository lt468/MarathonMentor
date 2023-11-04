import requests
from datetime import datetime
import urllib3
from ..models import StravaUserProfile, RunnerUser
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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

def get_strava_run(username):

    try:
        user = RunnerUser.objects.get(username=username)
        strava_profile = StravaUserProfile.objects.get(user=user)
    except Exception as e:
        print(f"No user or Strava account found: {e}")
    else:
        # URLs
        activites_url = "https://www.strava.com/api/v3/athlete/activities"

        access_token = strava_profile.strava_access_token

        # Get the latest n activities
        n = 5
        header = {'Authorization': 'Bearer ' + access_token} # Need to use the access token for the user you want to get the runs on 
        param = {'per_page': n, 'page': 1}
        my_dataset = requests.get(activites_url, headers=header, params=param).json()

        print("Activity Details:")
        print(my_dataset)

