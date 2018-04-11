"""Module for spotify gateway"""

from concurrent import futures
from spotipy import Spotify
from playlist_souffle.definitions.exception import SouffleParameterError
from playlist_souffle.definitions.playlist import Playlist
from playlist_souffle.gateways.spotify_util import (
    extract_playlist_uri_components,
    fetch_playlist_metadata,
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
    def fetch_playlist(self, playlist_uri):
        """Fetch a Playlist namedtuple representation of a spotify playlist given a playlist_uri."""
        user_id, playlist_id = extract_playlist_uri_components(playlist_uri)

        name, description = fetch_playlist_metadata(self._spotify, user_id, playlist_id)
        track_data = fetch_playlist_track_data(self._spotify, user_id, playlist_id)
        tracks = [pluck_track(track_record) for track_record in track_data]

        return Playlist(
            user_id=user_id,
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
            raise SouffleParameterError('Invalid shuffle_by type "{}".'.format(related_by))

        return related_tracks


    @raise_spotipy_error_as_souffle_error
    def fetch_related_tracks_by_track(self, tracks, related_by):
        """Fetch a related_tracks_by_track mapping, where each related_tracks set is the set of
        tracks related to a track in TRACKS by RELATED_BY.
        """
        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            related_tracks_by_track = dict(executor.map(
                lambda track: (track, self.fetch_related_tracks(track, related_by)),
                tracks
            ))

        return related_tracks_by_track


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
