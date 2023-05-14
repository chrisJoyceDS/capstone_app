from user_session import UserSession
import get_methods
import viz_model_methods
import streamlit as st
import pandas as pd
import pickle
import plotly
import numpy as np
import spotipy.oauth2 as oauth2

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

CATEGORY_OPTIONS = ['Tracks', 'Genres', 'Artists']
GENRES_LIST = []

def onboarding():
    user_session = UserSession()
    return user_session

def main():
    user_session = onboarding()

    # Check if 'access_token' is already in the session state
    if 'access_token' not in st.session_state:
        user_session.authenticate()
        st.session_state.access_token = user_session.access_token
        st.write("Successfully authenticated with Spotify API.")
        st.write("To begin, please provide two tracks you would like us to provide recommendations for:")    

    if st.session_state.access_token is not None:
        category = st.selectbox('Choose a category for recommendations', options=CATEGORY_OPTIONS, key='category')

        # Genres
        genres_container = st.container()
        
        with genres_container:
            
            if category == 'Genres':
                # Check if 'user_artist_list' is already in the session state
                if 'user_genres_list' not in st.session_state:
                    st.session_state.user_genre_list = []

                with st.form(key='genres_form'):
                    genre = st.text_input('Enter a genre')
                    submit_button = st.form_submit_button(label='Add Genre')
                    if submit_button:
                        st.session_state.user_artist_list.append(genre)
                        st.write(f"Added Genre: {genre}")
                        if len(st.session_state.user_artist_list) == 5:
                            st.write("You've reached the maximum number of Genres. Proceeding with these genres...")
                        # Display the list of artists
                        st.table(pd.DataFrame(st.session_state.user_genre_list))

                if len(st.session_state.user_genre_list) > 0:
                    df_genres = pd.DataFrame(st.session_state.user_genre_list)
                    st.table(df_genres)
                    
                if st.button('Click when ready to continue and get recommendations'):
                        # Here you can call your function to get recommendations
                        st.write('Getting recommendations...')
                        tracks_for_model = get_methods.search_genre_tracks(sp=st.session_state.access_token, genres=df_genres)
                        st.dataframe(tracks_for_model)
                        tracks_fig = viz_model_methods.visualize_signal(tracks_for_model)
                        st.pyplot(tracks_fig)
                        rec_songs_full, rec_songs = viz_model_methods.song_recommendations(tracks_for_model)
                        st.dataframe(rec_songs)
                        st.write("Let's Inspect our Rec Songs Audio Feature Distribution")
                        rec_fig = viz_model_methods.visualize_signal(rec_songs_full)
                        st.pyplot(rec_fig)
            else:
                genres_container.empty()
                
        # Artists
        artists_container = st.container()
        
        with artists_container:
            if category == 'Artists':
                # Check if 'user_artist_list' is already in the session state
                if 'user_artist_list' not in st.session_state:
                    st.session_state.user_artist_list = []

                with st.form(key='artists_form'):
                    artist_name = st.text_input('Enter an artist name')
                    submit_button = st.form_submit_button(label='Add Artist')
                    if submit_button:
                        st.session_state.user_artist_list.append(artist_name)
                        st.write(f"Added artist: {artist_name}")
                        if len(st.session_state.user_artist_list) == 5:
                            st.write("You've reached the maximum number of artists. Proceeding with these artists...")
                        # Display the list of artists
                        st.table(pd.DataFrame(st.session_state.user_artist_list))

                if len(st.session_state.user_artist_list) > 0:
                    df_artists = pd.DataFrame(st.session_state.user_artist_list)
                    st.table(df_artists)
                    
                if st.button('Click when ready to continue and get recommendations'):
                        # Here you can call your function to get recommendations
                        st.write('Getting recommendations...')
                        tracks_for_model = get_methods.search_artist_tracks(sp=st.session_state.access_token, artists=df_artists)
                        st.dataframe(tracks_for_model)
                        tracks_fig = viz_model_methods.visualize_signal(tracks_for_model)
                        st.pyplot(tracks_fig)
                        rec_songs_full, rec_songs = viz_model_methods.song_recommendations(tracks_for_model)
                        st.dataframe(rec_songs)
                        st.write("Let's Inspect our Rec Songs Audio Feature Distribution")
                        rec_fig = viz_model_methods.visualize_signal(rec_songs_full)
                        st.pyplot(rec_fig)
            else:
                artists_container.empty()
                
        # Tracks
        tracks_container = st.container()
        
        with tracks_container:
            
            if category == 'Tracks':
                # create st.session variables for tracks
                if 'user_track_list' not in st.session_state:
                    st.session_state.user_track_list = []
                
                with st.form(key='tracks_form'):
                    track_name = st.text_input('Enter a track name')
                    release_year = st.number_input('Enter the release year', min_value=1900, max_value=2023)
                    artist = st.text_input('Enter an artist name')
                    submit_button = st.form_submit_button(label='Add Track')
                    if submit_button:
                        st.session_state.user_track_list.append({"name": track_name, "artist": artist,
                                                                 "year": release_year})
                        st.write(f"Added track: {track_name}, Artist: {artist}, Release Year: {release_year}")
                        if len(st.session_state.user_track_list) == 5:
                            st.write("You've reached the maximum number of tracks. Proceeding with these tracks...")
                            
                if len(st.session_state.user_track_list) > 0:
                    df_tracks = pd.DataFrame(st.session_state.user_track_list)
                    st.table(df_tracks)

                    if st.button('Click when ready to continue and get recommendations'):
                        # Here you can call your function to get recommendations
                        st.write('Getting recommendations...')
                        tracks_for_model = get_methods.search_tracks(sp=st.session_state.access_token, tracks=df_tracks)
                        st.dataframe(tracks_for_model)
                        tracks_fig = viz_model_methods.visualize_signal(tracks_for_model)
                        st.pyplot(tracks_fig)
                        rec_songs_full, rec_songs = viz_model_methods.song_recommendations(tracks_for_model)
                        st.dataframe(rec_songs)
                        st.write("Let's Inspect our Rec Songs Audio Feature Distribution")
                        rec_fig = viz_model_methods.visualize_signal(rec_songs_full)
                        st.pyplot(rec_fig)
            else:
                tracks_container.empty()
    

        # saved_tracks = get_methods.handler(user_session, identifier='get_saved_tracks')
        # st.dataframe(saved_tracks).head()
        # st.write("Below is a representation of your Spotify Music Signal!")
        # st.write("Each violin represents a distribution of a different track audio feature. Where the violin is wider represents more records of those values, and the line in the middle represents the median of a given distribution.")
        # saved_fig = viz_model_methods.visualize_signal(saved_tracks)
        # st.pyplot(saved_fig)
        # st.write("Let's get you your first 10 song recommendations based on this signal!")
        # song_recs_full, song_recs = viz_model_methods.song_recommendations(saved_tracks)
        # st.dataframe(song_recs)
        # st.write("Now let's see how if your signal continues to show up in these recommendations and compare!")
        # rec_fig = viz_model_methods.visualize_signal(song_recs_full)
        # st.pyplot(rec_fig)
    # while user.access_token is not None:
    #     st.write("Sample of Playlist Tracks Will Load Here")
    #     user_playlist_tracks = get_methods.handler(user, "get_user_playlist_tracks")
    #     st.dataframe(user_playlist_tracks.loc[:,['track_name','artist','album','release_date','danceability']].head())
    #     playlist_fig = data_viz_methods.visualize_signal(user_playlist_tracks)
    #     st.pyplot(playlist_fig)
    #     break

if __name__ == "__main__":
    main()
