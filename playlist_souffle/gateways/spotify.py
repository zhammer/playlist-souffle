"""Module for spotify gateway"""

from concurrent import futures
from spotipy import Spotify
from playlist_souffle.definitions.exception import SouffleParameterError
from playlist_souffle.gateways.spotify_util import (
    extract_playlist_uri_components,
    fetch_playlist_track_data,
    pluck_track,
    raise_spotipy_error_as_souffle_error
)


class SpotifyGateway:
    """Class implementing spotify gateway."""

    @raise_spotipy_error_as_souffle_error
    def __init__(self, access_token):
        """C'tor"""
        self._spotify = Spotify(access_token, requests_session=False)


    @raise_spotipy_error_as_souffle_error
    def fetch_playlist_tracks(self, playlist_uri):
        """Fetch the tracks of a playlist as a list of Track namedtuples."""
        playlist_owner_id, playlist_id = extract_playlist_uri_components(playlist_uri)
        playlist_track_data = fetch_playlist_track_data(self._spotify, playlist_owner_id, playlist_id)
        return [pluck_track(track_record) for track_record in playlist_track_data]


    @raise_spotipy_error_as_souffle_error
    def fetch_playlist_name(self, playlist_uri):
        """Fetch the name of a playlist from spotify."""
        playlist_owner_id, playlist_id = extract_playlist_uri_components(playlist_uri)
        return self._spotify.user_playlist(playlist_owner_id, playlist_id, fields='name')['name']


    @raise_spotipy_error_as_souffle_error
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


    @raise_spotipy_error_as_souffle_error
    def fetch_collection_tracks_by_track(self, collection_id_by_track, collection_type):
        """Fetch a collection_tracks_by_collection_track mapping, given a collection_id_by_track
        mapping and a collection_type.
        """
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            collection_tracks_by_collection_id = dict(executor.map(
                lambda id: (id, self.fetch_collection_tracks(id, collection_type)),
                collection_id_by_track.values()
            ))

        return {track: collection_tracks_by_collection_id[collection_id]
                for track, collection_id in collection_id_by_track.items()}


    @raise_spotipy_error_as_souffle_error
    def create_playlist(self, playlist, is_public=True):
        """Create a new playlist for the given Playlist namedtuple.  Return the uri of the new
        playlist.
        """
        response = self._spotify.user_playlist_create(playlist.user_id, playlist.name, is_public)
        playlist_uri, playlist_id = response['uri'], response['id']

        playlist_track_ids = [track.id for track in playlist.tracks]
        self._spotify.user_playlist_add_tracks(playlist.user_id, playlist_id, playlist_track_ids)
        return playlist_uri
