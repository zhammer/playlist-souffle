"""Module for souffler entity util functions.

Available functions:
- generate_souffle_description: Generate a description for a souffled playlist.
- generate_souffle_name: Generate a name for a souffled playlist given its original name.
- souffle_tracks: Souffle a list of tracks, swapping out each track for a related track.
"""

import random
import re

SOUFFLE_NAME_RE = r'(?P<playlist_name>.*)\[souffle(?:\^(?P<souffle_degree>\d+))?\]$'
SOUFFLE_DESCRIPTION_FMT = 'Souffled from "{original_name}" by "{souffle_by}" at {time_of_souffle}.'


def generate_souffle_description(original_name, souffle_by, time_of_souffle):
    """Generate a description for a souffled playlist.

    >>> from datetime import datetime as dt
    >>> time_of_souffle = dt(1968, 11, 22, hour=9, minute=30, second=15)
    >>> generate_souffle_description('my playlist', 'artist', time_of_souffle)
    'Souffled from "my playlist" by "artist" at 1968-11-22 09:30:15.'
    """
    return SOUFFLE_DESCRIPTION_FMT.format(
        original_name=original_name,
        souffle_by=souffle_by,
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
        return '{} [souffle]'.format(original_name.rstrip())

    playlist_name = match.group('playlist_name').rstrip()
    souffle_degree = int(match.group('souffle_degree') or 1)

    return '{} [souffle^{}]'.format(playlist_name, souffle_degree + 1)


def souffle_tracks(tracks, related_tracks_by_track):
    """Souffle a list of tracks, swapping out each track for one of its related tracks based on the
    related_tracks_by_track mapping, given that the related track isn't in the original tracks and
    hasn't already been swapped to in the souffle_tracks operation.

    If there are no swappable tracks for a track -- meaning that all related tracks are either in
    the input tracks list or have already been swapped to -- the track will be swapped with itself.
    """
    tracks_set = set(tracks)
    souffled_tracks = []
    for track in tracks:
        related_tracks = related_tracks_by_track[track]
        swappable_tracks = related_tracks - tracks_set - set(souffled_tracks)
        souffled_track = random.sample(swappable_tracks, 1)[0] if swappable_tracks else track
        souffled_tracks.append(souffled_track)

    return souffled_tracks
