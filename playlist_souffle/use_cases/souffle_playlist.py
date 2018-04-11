"""Module for the souffle_playlist use case.

Available functions:
- souffle_playlist: Create a souffled playlist on a user's account given an original playlist.
"""

from datetime import datetime as dt
from playlist_souffle.definitions.playlist import Playlist
import playlist_souffle.entities.souffler as souffler_entity

def souffle_playlist(spotify, user_id, playlist_uri, shuffle_by):
    """Create a souffled playlist from an original playlist, where each track on the original
    playlist is swapped out with a related track, and save the souffled playlist to a user_id's
    account. The related tracks of a track are determined by shuffle_by. For instance, if shuffle_by
    is 'artist', each track wil be shuffled with another track by the same artist.
    """

    original_playlist = spotify.fetch_playlist(playlist_uri)

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
