"""Module for souffler entity.

Available functions:
- generate_souffled_playlist: Generate a souffled version of a Playlist namedtuple given a map of
  related_tracks_by_track for souffleing and other metadata.
"""

from playlist_souffle.definitions import Playlist
from playlist_souffle.entities.souffler_util import (
    generate_souffle_description,
    generate_souffle_name,
    souffle_tracks
)

def generate_souffled_playlist(original_playlist, souffle_by, related_tracks_by_track, souffle_time):
    """Given an original playlist, create a new playlist in which each track from the original
    playlist is swapped with one of its related tracks based on the related_tracks_by_track mapping.
    A 'souffled' name and description will be generated for the new playlist.
    """
    souffled_playlist_tracks = souffle_tracks(
        original_playlist.tracks,
        related_tracks_by_track
    )
    souffled_playlist_name = generate_souffle_name(original_playlist.name)
    souffled_playlist_description = generate_souffle_description(
        original_playlist.name,
        souffle_by,
        souffle_time
    )
    return Playlist(
        name=souffled_playlist_name,
        tracks=souffled_playlist_tracks,
        description=souffled_playlist_description
    )
