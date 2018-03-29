"""Module for souffler entity."""

import random
import re

SOUFFLE_NAME_RE = r'(.*)\[souffle(?:\^(\d+))?\]$'
SOUFFLE_NAME_NO_DEGREE_FMT = '{} [souffle]'
SOUFFLE_NAME_DEGREE_FMT = '{} [souffle^{}]'


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
    """Souffle a list of tracks using track_collections, a map of tracks to the set of tracks in
    each top-level track's collection.
    """
    souffled_tracks = []
    for track in tracks:
        collection_tracks = track_collections[track]
        valid_tracks = collection_tracks - {track} - set(souffled_tracks)
        souffled_track = random.sample(valid_tracks, 1)[0] if valid_tracks else track
        souffled_tracks.append(souffled_track)

    return souffled_tracks
