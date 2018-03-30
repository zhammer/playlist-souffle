"""Module for souffler entity."""

import random
import re

SOUFFLE_NAME_RE = r'(.*)\[souffle(?:\^(\d+))?\]$'
SOUFFLE_NAME_NO_DEGREE_FMT = '{} [souffle]'
SOUFFLE_NAME_DEGREE_FMT = '{} [souffle^{}]'
SOUFFLE_DESCRIPTION_FMT = 'Souffled from "{original_name}" by "{shuffle_by}" at {time_of_souffle}.'

def generate_souffle_description(original_name, shuffle_by, time_of_souffle):
    """Generate a description for a souffled playlist.

    >>> from datetime import datetime as dt
    >>> time_of_souffle = dt(1968, 11, 22, hour=9, minute=30, second=15)
    >>> generate_souffle_description('my playlist', 'artist', time_of_souffle)
    'Souffled from "my playlist" by "artist" at 1968-11-22 09:30:15.'
    """
    return SOUFFLE_DESCRIPTION_FMT.format(
        original_name=original_name,
        shuffle_by=shuffle_by,
        time_of_souffle=time_of_souffle
    )


def generate_souffle_name(original_name):
    """Generate the name of a souffled playlist. On a non-souffled playlist, add [souffle] to the
    end of playlist name. On a souffled playlist -- a playlist ending in [souffle] -- increment
    degree, i.e "[souffle^2]".

    >>> generate_souffle_name('my playlist')
    'my playlist [souffle]'

    >>> generate_souffle_name('my playlist [souffle]')
    'my playlist [souffle^2]'

    >>> generate_souffle_name('my playlist [souffle^3]')
    'my playlist [souffle^4]'

    >>> generate_souffle_name('my playlist [souffle^130]')
    'my playlist [souffle^131]'
    """
    match = re.match(SOUFFLE_NAME_RE, original_name)

    if not match:
        return SOUFFLE_NAME_NO_DEGREE_FMT.format(original_name.rstrip())

    playlist_name = match.group(1).rstrip()
    souffle_degree = int(match.group(2) or 1)

    return SOUFFLE_NAME_DEGREE_FMT.format(playlist_name, souffle_degree + 1)


def souffle_tracks(tracks, track_collections):
    """Souffle a list of tracks, swapping out each track for another track on its collection,
    using track_collections: a dict mapping tracks in 'tracks' to the set of tracks in their
    collections.
    """
    tracks_set = set(tracks)
    souffled_tracks = []
    for track in tracks:
        collection_tracks = track_collections[track]
        valid_tracks = collection_tracks - tracks_set - set(souffled_tracks)
        souffled_track = random.sample(valid_tracks, 1)[0] if valid_tracks else track
        souffled_tracks.append(souffled_track)

    return souffled_tracks
