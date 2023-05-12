import spotipy
import spotipy.oauth2 as oauth2
import webbrowser
import os
import requests
import streamlit as st

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

        # Display the authorization URL to the user
        st.write('Please visit the following URL and enter the code that you get when you authenticate:')
        st.write(auth_url)

        # Get the code from the user
        code = st.text_input('Enter the code: ')

        # Get the access token
        token_info = auth.get_access_token(code)
        access_token = token_info['access_token']

        # Create a Spotify client
        sp = spotipy.Spotify(auth=access_token)
        self.access_token = sp


