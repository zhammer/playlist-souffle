"""Module for souffler entity."""

from playlist_souffle.definitions.playlist import Playlist
from playlist_souffle.entities.souffler_util import (
    generate_souffle_description,
    generate_souffle_name,
    souffle_tracks
)

def generate_souffled_playlist(original_playlist, user_id, shuffle_by, collection_tracks_by_track, souffle_time):
    """Generate a souffled playlist given a Playlist namedtuple of the original playlist and a
    collection_tracks_by_track mapping for souffleing. Returns a Playlist namedtuple.
    """
    souffled_playlist_tracks = souffle_tracks(
        original_playlist.tracks,
        collection_tracks_by_track
    )
    souffled_playlist_name = generate_souffle_name(original_playlist.name)
    souffled_playlist_description = generate_souffle_description(
        original_playlist.name,
        shuffle_by,
        souffle_time
    )
    return Playlist(
        user_id=user_id,
        name=souffled_playlist_name,
        tracks=souffled_playlist_tracks,
        description=souffled_playlist_description
    )
