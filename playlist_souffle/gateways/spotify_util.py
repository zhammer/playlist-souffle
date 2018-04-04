"""Module for spotify gateway util functions"""

import functools
import spotipy
from playlist_souffle.definitions.track import Track
from playlist_souffle.definitions.exception import SouffleParameterError, SouffleSpotifyError

SPOTIFY_PLAYLIST_FIELDS = 'items(track(id, artists.id, album.id))'


def raise_spotipy_error_as_souffle_error(func):
    """Decorator that raises spotipy Spotify errors as souffle Spotify errors."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except spotipy.SpotifyException as e:
            raise SouffleSpotifyError(
                http_status=e.http_status,
                message=e.msg
            )
    return inner


def extract_playlist_uri_components(playlist_uri):
    """Extract the user_id and playlist_id of a playlist from its spotify uri.
    Raises a SouffleParameterError if playlist uri isn't correctly formatted.

    >>> extract_playlist_uri_components('spotify:user:MY_USER:playlist:MY_PLAYLIST')
    ('MY_USER', 'MY_PLAYLIST')
    """
    components = playlist_uri.split(':')
    try:
        return components[2], components[4]
    except IndexError:
        raise SouffleParameterError('Invalid playlist uri: "{}"'.format(playlist_uri))


def pluck_track(track_record, artist=None, album=None):
    """Pluck a Track namedtuple from a spotify api track object.
    Artist and album default values may be provided, in which case those field's data will not be
    extracted from the provided track data.

    Note: If there are multiple artists on a track, the plucked track will only contain the id of
    the first artist listed.

    """
    return Track(
        id=track_record['id'],
        artist=(artist or track_record['artists'][0]['id']),
        album=(album or track_record['album']['id'])
    )


def fetch_playlist_track_data(spotify, user_id, playlist_id):
    """Fetch a list of spotify api track objects as raw data. Only fetch the track.id,
    track.artists.id, and track.album.id fields.

    """
    response = spotify.user_playlist_tracks(
        user_id,
        playlist_id,
        fields=SPOTIFY_PLAYLIST_FIELDS
    )
    return [item['track'] for item in response['items']]
