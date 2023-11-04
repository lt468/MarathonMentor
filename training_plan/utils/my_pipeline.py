import requests
import urllib3
from decouple import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def save_profile(backend, user, response, *args, **kwargs):
    try:
        client_id = response["athlete"]["id"]
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        expires_at = response["expires_at"]
        firstname = response["athlete"]["firstname"]
        lastname = response["athlete"]["lastname"]
        print("User Details:")
        print(f"Client ID: {client_id}")
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print(f"Expires At: {expires_at}")
        print(f"First Name: {firstname}")
        print(f"Last Name: {lastname}")
        auth_url = "https://www.strava.com/api/v3/oauth/token"
        activites_url = "https://www.strava.com/api/v3/athlete/activities"

        # Strava API credentials
        client_id = config("STRAVA_CLIENT_ID")
        client_secret = config("STRAVA_CLIENT_SECRET")
        refresh_token = config("STRAVA_REFRESH_TOKEN")

        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': "refresh_token",
            'f': 'json'
        }

        print("Requesting Token...\n")
        res = requests.post(auth_url, data=payload, verify=False)
        #access_token = res.json()['access_token']
        print("Access Token = {}\n".format(access_token))

        header = {'Authorization': 'Bearer ' + access_token} # Need to use the access token for the user you want to get the runs on 
        param = {'per_page': 1, 'page': 1}
        my_dataset = requests.get(activites_url, headers=header, params=param).json()

        print("Activity Details:")
        print(my_dataset)
    except Exception as e:
        print("Error while retrieving user details:", e)

