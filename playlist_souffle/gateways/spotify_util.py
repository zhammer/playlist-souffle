"""Module for spotify gateway util functions"""

from playlist_souffle.definitions.track import Track
from playlist_souffle.definitions.exception import SouffleParameterError

SPOTIFY_PLAYLIST_FIELDS = 'items(track(id, artists.id, album.id))'

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


def fetch_playlist_track_data(user_id, playlist_id, spotify):
    """Fetch a list of spotify api track objects as raw data. Only fetch the track.id,
    track.artists.id, and track.album.id fields.

    """
    response = spotify.user_playlist_tracks(
        user_id,
        playlist_id,
        fields=SPOTIFY_PLAYLIST_FIELDS
    )
    return [item['track'] for item in response['items']]


def create_playlist(user_id, playlist_name, public, description, spotify):
    """Create a playlist for USER_ID with name PLAYLIST_NAME. Return its uri and id as a tuple."""
    # NOTE: It seems PR #196 for spotipy, adding description support, was never added.
    response = spotify.user_playlist_create(user_id, playlist_name, public)
    return response['uri'], response['id']


def add_tracks_to_playlist(user_id, playlist_id, tracks, spotify):
    """Add tracks to a playlist."""
    spotify.user_playlist_add_tracks(user_id, playlist_id, [track.id for track in tracks])
