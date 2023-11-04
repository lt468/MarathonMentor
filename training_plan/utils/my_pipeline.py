from ..models import StravaUserProfile

def save_profile(backend, user, response, *args, **kwargs):
    try:
        client_id = response["athlete"]["id"]
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        expires_at = response["expires_at"]
        firstname = response["athlete"]["firstname"]
        lastname = response["athlete"]["lastname"]
        print(client_id, firstname, lastname, access_token)
    except Exception as e:
        print(e, e.args)


