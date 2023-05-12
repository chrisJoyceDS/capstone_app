# User Playlist Tracks
def get_user_playlist_tracks(sp):
    """
    Retrieves the user's playlists and tracks for each playlist and adds them to a DataFrame.
    :param sp: a spotipy.Spotify object with an access token for the user
    :param df: a dataframe made up of a user's liked tracks and their audio features
    :return: a pandas DataFrame containing playlist name, track ID, track name, and track artists
    """
    # get lists of playlist ids 
    playlist_ids = get_user_playlists(sp)
    
    # set new list for flattened tracks
    tracks = []
    # loop through zippled playlist ids and names
    for playlist_id in playlist_ids:
        # get tracks from playlist
        tracks.extend(get_all_playlist_tracks(sp, playlist_id))
        
    
    # turn flattened tracks into pandas df and return
    playlist_tracks_df = pd.DataFrame(flatten_tracks(tracks))

        
    return playlist_tracks_df

def get_all_playlist_tracks(sp, playlist_id):
    """
    Retrieves the tracks contained in a playlist object by passing the playlist id
    :param sp: a spotipy.Spotify object with an access token for the user
    :param playlist_id: id associated to a specific Spotify playlist
    :return tracks: a list of track objects from the current playlist
    """
    # results = specific playlist
    results = sp.playlist_items(playlist_id)
    # tracks equals items key value pair
    tracks = results['items']
    # the playlist_tracks call has a limit of 100,
    # when there are more tracks, the response contains a next url
    while results['next']:
        # the next function takes a previous paged result and generates the next
        results = sp.next(results)
        # extend tracks by next call
        tracks.extend(results['items'])
    # return tracks
    return tracks
