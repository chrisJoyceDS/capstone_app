import get_methods
import viz_model_methods
import streamlit as st
import pandas as pd
import pickle
import plotly
import numpy as np
import os

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
# create oauth object
oauth = SpotifyOAuth(scope='user-library-read user-top-read playlist-read-private user-follow-read',
                     redirect_uri=uri,
                     client_id=cid,
                     client_secret=csecret)
# Set up the page
st.set_page_config(page_title="What's your Spotify Signal?", page_icon=":bar_chart:", layout="wide")



# Set up the sidebar
st.sidebar.title("Project Authors")
st.sidebar.info(
    "This application was created by [Chris Joyce](https://github.com/chrisJoyceDS)."
)

st.sidebar.title("GitHub Repository")
st.sidebar.info(
    "[Link to the public GitHub repository](https://github.com/chrisJoyceDS/spotify-signal)."
)

def get_token(oauth, code):

    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    # remove cached token saved in directory
    os.remove(".cache")
    
    # return the token
    return token

def sign_in(token):
    sp = spotipy.Spotify(auth=token)
    return sp

def app_get_token():
    try:
        token = get_token(st.session_state["oauth"], st.session_state["code"])
    except Exception as e:
        st.error("An error occurred during token retrieval!")
        st.write("The error is as follows:")
        st.write(e)
    else:
        st.session_state["cached_token"] = token

def app_sign_in():
    try:
        sp = sign_in(st.session_state["cached_token"])
    except Exception as e:
        st.error("An error occurred during sign-in!")
        st.write("The error is as follows:")
        st.write(e)
    else:
        st.session_state["signed_in"] = True
        app_display_welcome()
        st.success("Sign in success!")
        
    return sp        
        
        
def main():
    # user = onboarding()
    st.title("Using Spotify App Data to Visualize your Signal")
    st.write("Problem Statement:")
    st.write("""Loaded to the gunwalls scuttle coxswain barque lateen sail Arr mutiny yo-ho-ho Shiver me timbers topgallant. Ahoy clap of thunder topmast Corsair hands yard heave to line Cat o'nine tails scourge of the seven seas. Rigging wherry dead men tell no tales chase guns hogshead execution dock tender coffer provost cable.""")
    st.write("""For this Web App to perform we will need you as a user to authenticate access to the Spotify API for your individual profile. Before you choose yes or no, please see what access we will be asking for below:""")
    items = ['user-library-read: Access your saved content.', 'user-top-read: Read your top artists and content.', 'playlist-read-private: Access your private playlists.', 'user-follow-read: Access your followers and who you are following.']
    for i, item in enumerate(items, start=1):
        st.write(f"{i}. {item}")
    st.write("If these permissions are okay, please click the Authenticate button below to get started.")
    
    # store oauth in session
    st.session_state["oauth"] = oauth
    
    # retrieve auth url
    auth_url = oauth.get_authorize_url()
    
    # this SHOULD open the link in the same tab when Streamlit Cloud is updated
    # via the "_self" target
    link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Click me to authenticate!"
    )
    
    # define temporary note
    note_temp = """
    _Note: Unfortunately, the current version of Streamlit will not allow for
    staying on the same page, so the authorization and redirection will open in a 
    new tab. This has already been addressed in a development release, so it should
    be implemented in Streamlit Cloud soon!_
    """
    
    if not st.session_state["signed_in"]:
        st.write(" ".join(["No tokens found for this session. Please log in by",
                          "clicking the link below."]))
        st.markdown(link_html, unsafe_allow_html=True)
        
    # %% app session variable initialization

    if "signed_in" not in st.session_state:
        st.session_state["signed_in"] = False
    if "cached_token" not in st.session_state:
        st.session_state["cached_token"] = ""
    if "code" not in st.session_state:
        st.session_state["code"] = ""
    if "oauth" not in st.session_state:
        st.session_state["oauth"] = None
        
    # get current url (stored as dict)
    url_params = st.experimental_get_query_params()
    
    # attempt sign in with cached token
    if st.session_state["cached_token"] != "":
        sp = app_sign_in()
    # if no token, but code in url, get code, parse token, and sign in
    elif "code" in url_params:
        # all params stored as lists, see doc for explanation
        st.session_state["code"] = url_params["code"][0]
        app_get_token()
        sp = app_sign_in()
    # otherwise, prompt for redirect
    else:
        st.write('FUCK YOU')
        
    
    
    if st.session_state["signed_in"]:
        saved_tracks = get_methods.handler(user, identifier='get_saved_tracks')
        st.write("Below is a representation of your Spotify Music Signal!")
        st.write("Each violin represents a distribution of a different track audio feature. Where the violin is wider represents more records of those values, and the line in the middle represents the median of a given distribution.")
        saved_fig = viz_model_methods.visualize_signal(saved_tracks)
        st.pyplot(saved_fig)
        st.write("Let's get you your first 10 song recommendations based on this signal!")
        song_recs_full, song_recs = viz_model_methods.song_recommendations(saved_tracks)
        st.dataframe(song_recs)
        st.write("Now let's see how if your signal continues to show up in these recommendations and compare!")
        rec_fig = viz_model_methods.visualize_signal(song_recs_full)
        st.pyplot(rec_fig)
        
    # while user.access_token is not None:
    #     st.write("Sample of Playlist Tracks Will Load Here")
    #     user_playlist_tracks = get_methods.handler(user, "get_user_playlist_tracks")
    #     st.dataframe(user_playlist_tracks.loc[:,['track_name','artist','album','release_date','danceability']].head())
    #     playlist_fig = data_viz_methods.visualize_signal(user_playlist_tracks)
    #     st.pyplot(playlist_fig)
    #     break

if __name__ == "__main__":
    main()
