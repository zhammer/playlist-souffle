"""Module for spotify gateway"""

from spotipy import Spotify
from playlist_souffle.definitions.exception import SouffleParameterError
from playlist_souffle.gateways.spotify_util import (
    add_tracks_to_playlist,
    create_playlist,
    extract_playlist_uri_components,
    fetch_playlist_track_data,
    pluck_track
)


class SpotifyGateway:
    """Class implementing spotify gateway."""

    def __init__(self, access_token):
        """C'tor"""
        self._spotify = Spotify(access_token)


    def fetch_playlist_tracks(self, playlist_uri):
        """Fetch the tracks of a playlist as a list of Track namedtuples."""
        playlist_owner_id, playlist_id = extract_playlist_uri_components(playlist_uri)
        playlist_track_data = fetch_playlist_track_data(playlist_owner_id, playlist_id, self._spotify)
        return [pluck_track(track_record) for track_record in playlist_track_data]


    def fetch_playlist_name(self, playlist_uri):
        """Fetch the name of a playlist from spotify."""
        playlist_owner_id, playlist_id = extract_playlist_uri_components(playlist_uri)
        return self._spotify.user_playlist(playlist_owner_id, playlist_id, fields='name')['name']


    def fetch_collection_tracks(self, collection_id, collection_type):
        """Fetch a set of Track namedtuples in a collection of collection_type."""
        if collection_type == 'artist':
            track_data = self._spotify.artist_top_tracks(collection_id)['tracks']
            tracks = {pluck_track(track_record, artist=collection_id) for track_record in track_data}

        elif collection_type == 'album':
            track_data = self._spotify.album_tracks(collection_id)['items']
            tracks = {pluck_track(track_record, album=collection_id) for track_record in track_data}

        else:
            raise SouffleParameterError('Invalid shuffle_by type "{}".'.format(collection_type))

        return tracks


    def create_playlist_with_tracks(self, user_id, playlist_name, tracks, public=True, description=''):
        """Create a new playlist for USER_ID with TRACKS. Return the uri of the new playlist."""
        playlist_uri, playlist_id = create_playlist(user_id, playlist_name, public, description, self._spotify)
        add_tracks_to_playlist(user_id, playlist_id, tracks, self._spotify)
        return playlist_uri
