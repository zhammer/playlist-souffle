"""Module for the spotify gateway.

Available classes:
- SpotifyGateway: Gateway class for interfacing with the spotify web api.
"""

from concurrent import futures
from spotipy import Spotify
import requests
from playlist_souffle.definitions.exception import SouffleParameterError
from playlist_souffle.definitions import Playlist
from playlist_souffle.gateways.spotify_util import (
    BASE,
    fetch_playlist_metadata,
    fetch_playlist_track_data,
    pluck_track,
    raise_spotipy_error_as_souffle_error
)


class SpotifyGateway:
    """Class implementing a gateway to the spotify web api.

    Available functions:
    - fetch_playlist: Fetch a Playlist namedtuple given a playlist_uri.
    - fetch_related_tracks: Fetch a track's related tracks by artist or album.
    - fetch_related_tracks_by_track: Concurrently fetch a mapping of tracks to their related tracks.
    - create_playlist: Create a playlist for a user[]
    """

    @raise_spotipy_error_as_souffle_error
    def __init__(self, access_token: str):
        """C'tor"""
        self._access_token = access_token
        self._spotify = Spotify(access_token, requests_session=False)


    @raise_spotipy_error_as_souffle_error
    def fetch_playlist(self, playlist_uri: str):
        """Fetch a Playlist namedtuple representation of a spotify playlist given a playlist_uri."""
        playlist_id = playlist_uri.split(':')[-1]

        name, description = fetch_playlist_metadata(playlist_id, self._access_token)
        track_data = fetch_playlist_track_data(playlist_id, self._access_token)
        tracks = [pluck_track(track_record) for track_record in track_data]

        return Playlist(
            name=name,
            tracks=tracks,
            description=description
        )


    @raise_spotipy_error_as_souffle_error
    def fetch_related_tracks(self, track, related_by):
        """Fetch a set of Track namedtuples that are related to TRACK by RELATED_BY."""
        if related_by == 'artist':
            related_track_data = self._spotify.artist_top_tracks(track.artist)['tracks']
            related_tracks = {pluck_track(track_record, artist=track.artist)
                              for track_record in related_track_data}

        elif related_by == 'album':
            related_track_data = self._spotify.album_tracks(track.album)['items']
            related_tracks = {pluck_track(track_record, album=track.album)
                              for track_record in related_track_data}

        else:
            raise SouffleParameterError('Invalid souffle type "{}".'.format(related_by))

        return related_tracks


    @raise_spotipy_error_as_souffle_error
    def fetch_related_tracks_by_track(self, tracks, related_by):
        """Fetch a related_tracks_by_track mapping, where each related_tracks set is the set of
        tracks related to a track in TRACKS by RELATED_BY.
        """
        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            related_tracks_by_track = dict(executor.map(
                lambda track: (track, self.fetch_related_tracks(track, related_by)),
                tracks
            ))

        return related_tracks_by_track


    @raise_spotipy_error_as_souffle_error
    def create_playlist(self, playlist: Playlist, is_public: bool = True) -> str:
        """Create a new playlist for the given Playlist namedtuple.  Return the uri of the new
        playlist.
        """
        user_id = self.fetch_current_user_id()
        response = requests.post(
            f'{BASE}/users/{user_id}/playlists',
            json={
                'name': playlist.name,
                'description': playlist.description,
                'public': is_public
            },
            headers={'Authorization': f'Bearer {self._access_token}'}
            )
        response_json = response.json()
        playlist_id = response_json['id']
        playlist_track_uris = [f'spotify:track:{track.id}' for track in playlist.tracks]
        response = requests.post(
            f'{BASE}/playlists/{playlist_id}/tracks',
            params={
                'uris': ','.join(playlist_track_uris)
            },
            headers={'Authorization': f'Bearer {self._access_token}'}
            )
        return playlist_id


    @raise_spotipy_error_as_souffle_error
    def fetch_current_user_id(self):
        """Fetch the current user id based on the access token provided to the SpotifyGateway
        constructor.

        Note: This should eventually return a plucked User namedtuple.
        """
        response = self._spotify.current_user()
        return response['id']
