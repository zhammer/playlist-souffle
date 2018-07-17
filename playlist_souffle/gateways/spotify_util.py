"""Module for spotify gateway util functions.

Available decorators:
- raise_spotipy_error_as_souffle_error: Re-raise spotipy.SpotifyErrors as SouffleSpotifyErrors.

Available functions:
- extract_playlist_uri_components: Extract the user_id and playlist_id of a spotify playlist uri.
- fetch_playlist_metadata: Fetch the name and description of a spotify playlist.
- fetch_playlist_track_data: Fetch a list of raw spotify web api track objects of a playlist.
- pluck_track: Pluck a Track namedtuple froma raw spotify web api track object.

"""

import functools
import spotipy
from playlist_souffle.definitions import Track
from playlist_souffle.definitions.exception import SouffleParameterError, SouffleSpotifyError

SPOTIFY_PLAYLIST_METADATA_FIELDS = 'name, description'
SPOTIFY_PLAYLIST_TRACK_FIELDS = 'items(track(id, artists.id, album.id))'


def raise_spotipy_error_as_souffle_error(func):
    """Decorator that catches `SpotifyError`s eminating from the spotipy library in a decorated
    function and re-raises them as `SouffleSpotifyError`s.
    """
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


def fetch_playlist_metadata(spotify, user_id, playlist_id):
    """Fetch the name and description of a spotify playlist given its user_id and playlist_id."""
    response = spotify.user_playlist(
        user_id,
        playlist_id,
        fields=SPOTIFY_PLAYLIST_METADATA_FIELDS
    )

    return response['name'], response['description']


def fetch_playlist_track_data(spotify, user_id, playlist_id):
    """Fetch a list of spotify api track objects as raw data. Only fetch the track.id,
    track.artists.id, and track.album.id fields.

    """
    response = spotify.user_playlist_tracks(
        user_id,
        playlist_id,
        fields=SPOTIFY_PLAYLIST_TRACK_FIELDS
    )
    return [item['track'] for item in response['items']]
