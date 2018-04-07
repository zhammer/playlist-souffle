"""Module for the souffle_playlist use case."""

from datetime import datetime as dt
from playlist_souffle.definitions.playlist import Playlist
import playlist_souffle.entities.souffler as souffler_entity

def souffle_playlist(spotify, user_id, playlist_uri, shuffle_by):
    """Souffle a playlist."""

    original_playlist = Playlist(
        user_id=None,
        name=spotify.fetch_playlist_name(playlist_uri),
        tracks=spotify.fetch_playlist_tracks(playlist_uri),
        description=None
    )

    related_tracks_by_track = spotify.fetch_related_tracks_by_track(
        original_playlist.tracks,
        related_by=shuffle_by
    )

    souffled_playlist = souffler_entity.generate_souffled_playlist(
        original_playlist,
        user_id,
        shuffle_by,
        related_tracks_by_track,
        souffle_time=dt.now()
    )

    souffled_playlist_uri = spotify.create_playlist(souffled_playlist)

    return souffled_playlist_uri
