import os
import spotipy
import spotipy.oauth2 as oauth2
import webbrowser
import streamlit as st
import time

# load Spotify OAuth credentials from .env file
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
PORT_NUMBER = 8080
# Set scope for Spotify authorization
SCOPE = "user-top-read"
CACHE = '.spotipyoauthcache'
###############

###############
# Define function to authenticate user with Spotify
def authenticate(scope):
    """
    Instantiates a connection object through Spotipy for a Spotify Web API session. Uses env variables
    for client, client secret, and client redirect URI to handle request. Checks to see if there is a cached token for use. If there is, sets the access token to the current cached token. If not, it retrieves an authorization url to redirect the user to, and creates a prompt for the user to paste the code in from the site they visited. After code is entered, retrieves an access token via the auth_code provided, and saves it as an access token. Finally a Spotify session object is created with the access token which last 1hr before needing to be refreshed.
    :param scope: a scope string which provides different access to different calls and data from Spotify.
    :return sp: a spotipy.Spotify object with an access token for the user
    """
    # Scopes for the API access
    scope = 'user-read-currently-playing playlist-read-private user-read-private user-top-read'

    # Create an instance of SpotifyOAuth
    auth = oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                               client_secret=CLIENT_SECRET,
                               redirect_uri=REDIRECT_URI,
                               scope=scope,
                               cache_path=CACHE)

    # Generate the authorization URL
    auth_url = auth.get_authorize_url()

    # Open the URL in a web browser
    webbrowser.open(auth_url)

    # Get the access token
    token_info = auth.get_access_token()
    access_token = token_info['access_token']

    # Create a Spotify client
    sp = spotipy.Spotify(auth=access_token)

#     # set up OAuth2 flow
#     auth = oauth2.SpotifyOAuth(client_id=CLIENT_ID,
#                                client_secret=CLIENT_SECRET,
#                                redirect_uri=REDIRECT_URI,
#                                scope=scope,
#                                cache_path=CACHE)
#     # check if there is a cached access token
#     cached_token = auth.get_cached_token()
#     # if cached token is populated
#     if cached_token:
#         # use cached token
#         access_token = cached_token['access_token']
#     else:
#         # get authorization URL and prompt user to authorize the app
#         auth_url = auth.get_authorize_url()
#         webbrowser.open(auth_url, new=1)
#         auth_code = input("Enter the authorization code: ")

#         # exchange authorization code for access token and refresh token
#         token_info = auth.get_access_token(auth_code)
#         access_token = token_info['access_token']
        
#     sp = spotipy.Spotify(auth=access_token) 
    
    return sp

# Define Streamlit app
def app():
    # Set app title
    st.set_page_config(page_title="Spotify App")
    st.title("Welcome to the Spotify App")

    # Authenticate user with Spotify
    sp = authenticate(SCOPE)

    # Check if user is authenticated
    if sp:
        # Get user's top tracks
        top_tracks = sp.current_user_top_tracks(limit=10, time_range="medium_term")
        
        # Display user's top tracks on app screen
        st.write("Your top 10 tracks:")
        for track in top_tracks["items"]:
            st.write("- {} by {}".format(track["name"], track["artists"][0]["name"]))
        
        # Logout button
        if st.button("Logout"):
            # Clear cache and logout
            util.prompt_for_user_token(username=None, scope=None, client_id=None, client_secret=None, redirect_uri=None)
            st.write("You have successfully logged out.")
    # else:
    #     # Login button
    #     if st.button("Login with Spotify"):
    #         # Authenticate user with Spotify
    #         sp = authenticate()
    #         # If authentication successful, display user's top tracks on app screen
    #         if sp:
    #             top_tracks = sp.current_user_top_tracks(limit=10, time_range="medium_term")
    #             st.write("Your top 10 tracks:")
    #             for track in top_tracks["items"]:
    #                 st.write("- {} by {}".format(track["name"], track["artists"][0]["name"]))
    #         else:
    #             st.write("Authentication failed. Please try again.")
app()