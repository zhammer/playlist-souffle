"""Module for spotify gateway"""

from spotipy import Spotify
from playlist_souffle.definitions.exception import SouffleParameterError
from playlist_souffle.gateways.spotify_util import (
    add_tracks_to_playlist,
    create_playlist,
    extract_playlist_uri_components,
    fetch_playlist_track_data,
    pluck_tracks_as_list,
    pluck_tracks_as_set
)


class SpotifyGateway:
    """Class implementing spotify gateway."""

    def __init__(self, access_token):
        """C'tor"""
        self._spotify = Spotify(access_token)


    def fetch_playlist_tracks(self, playlist_uri):
        """Fetch the tracks of a playlist as a list of Track namedtuples."""
        return SpotifyGateway._fetch_playlist_tracks(playlist_uri, self._spotify)


    def fetch_playlist_name(self, playlist_uri):
        """Fetch the name of a playlist from spotify."""
        return SpotifyGateway._fetch_playlist_name(playlist_uri, self._spotify)


    def fetch_collection_tracks(self, collection_id, collection_type):
        """Fetch a set of Track namedtuples in a collection of collection_type."""
        return SpotifyGateway._fetch_collection_tracks(
            collection_id,
            collection_type,
            self._spotify
        )


    def create_playlist_with_tracks(self, user_id, playlist_name, tracks, public=True, description=''):
        """Create a new playlist for USER_ID with TRACKS. Return the uri of the new playlist."""
        return SpotifyGateway._create_playlist_with_tracks(
            user_id,
            playlist_name,
            tracks,
            public,
            description,
            self._spotify
        )


    @staticmethod
    def _fetch_playlist_tracks(playlist_uri, spotify):
        """Fetch the tracks of a playlist as a list of Track namedtuples."""
        playlist_owner_id, playlist_id = extract_playlist_uri_components(playlist_uri)
        playlist_track_data = fetch_playlist_track_data(playlist_owner_id, playlist_id, spotify)
        return pluck_tracks_as_list(playlist_track_data)


    @staticmethod
    def _fetch_playlist_name(playlist_uri, spotify):
        """Fetch the name of a playlist from spotify."""
        playlist_owner_id, playlist_id = extract_playlist_uri_components(playlist_uri)
        return spotify.user_playlist(playlist_owner_id, playlist_id, fields='name')['name']


    @staticmethod
    def _fetch_collection_tracks(collection_id, collection_type, spotify):
        """Fetch the set of Track namedtuples in a collection of collection_type."""
        if collection_type == 'artist':
            track_data = spotify.artist_top_tracks(collection_id)['tracks']
            tracks = pluck_tracks_as_set(track_data, artist=collection_id)

        elif collection_type == 'album':
            track_data = spotify.album_tracks(collection_id)['items']
            tracks = pluck_tracks_as_set(track_data, album=collection_id)

        else:
            raise SouffleParameterError('Invalid shuffle_by type "{}".'.format(collection_type))

        return tracks


    @staticmethod
    def _create_playlist_with_tracks(user_id, playlist_name, tracks, spotify):
        """Create a new playlist for USER_ID with TRACKS. Return the uri & id of the new playlist"""
        playlist_uri, playlist_id = create_playlist(user_id, playlist_name, spotify)
        add_tracks_to_playlist(user_id, playlist_id, tracks, spotify)
        return playlist_uri
