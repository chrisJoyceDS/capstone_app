import spotipy
import spotipy.oauth2 as oauth2
import webbrowser
import os
import requests

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

class User:
    
    def __init__(self):
        self.authed = False
        self.access_token = None

    def authenticate(self):
        
        # Scopes for the API access
        scope = 'user-library-read user-top-read playlist-read-private user-follow-read'

        # Create an instance of SpotifyOAuth
        auth = oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri=REDIRECT_URI,
                                   scope=scope)

        # Generate the authorization URL
        auth_url = auth.get_authorize_url()

        # Make a request to the authorization URL
        response = requests.get(auth_url)

        # Parse the response to get the access token
        access_token = response.json()['access_token']
        
        # Create a Spotify client
        sp = spotipy.Spotify(auth=access_token)
        self.access_token = sp

