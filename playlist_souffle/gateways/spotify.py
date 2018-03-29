"""Module for spotify gateway"""

from spotipy import Spotify
from playlist_souffle.definitions.track import Track
from playlist_souffle.definitions.exception import SouffleParameterError

_SPOTIFY_PLAYLIST_FIELDS = 'items(track(id, artists.id, album.id))'

def _extract_playlist_uri_components(playlist_uri):
    """Extract the user_id and playlist_id of a playlist from its spotify uri.
    Raises a SouffleParameterError if playlist uri isn't correctly formatted.

    >>> _extract_playlist_uri_components('spotify:user:MY_USER:playlist:MY_PLAYLIST')
    ('MY_USER', 'MY_PLAYLIST')
    """
    components = playlist_uri.split(':')
    try:
        return components[2], components[4]
    except IndexError:
        raise SouffleParameterError('Invalid playlist uri: "{}"'.format(playlist_uri))


def _pluck_track(track_record, artist=None, album=None):
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


def _pluck_tracks_as_list(track_records, artist=None, album=None):
    """Pluck list of Track namedtuples from a list of spotify api track objects.
    Artist and album default values may be provided, in which case those field's data will not be
    extracted from the provided track data.

     Note: If there are multiple artists on a track, the plucked track will only contain the id of
    the first artist listed.

    """
    return [_pluck_track(track_record, artist, album) for track_record in track_records]


def _pluck_tracks_as_set(track_records, artist=None, album=None):
    """Pluck list of Track namedtuples from a list of spotify api track objects.
    Artist and album default values may be provided, in which case those field's data will not be
    extracted from the provided track data.

    Note: If there are multiple artists on a track, the plucked track will only contain the id of
    the first artist listed.

    """
    return {_pluck_track(track_record, artist, album) for track_record in track_records}


def _fetch_playlist_track_data(user_id, playlist_id, spotify):
    """Fetch a list of spotify api track objects as raw data. Only fetch the track.id,
    track.artists.id, and track.album.id fields.

    """
    response = spotify.user_playlist_tracks(
        user_id,
        playlist_id,
        fields=_SPOTIFY_PLAYLIST_FIELDS
    )
    return [item['track'] for item in response['items']]


def _create_playlist(user_id, playlist_name, spotify):
    """Create a playlist for USER_ID with name PLAYLIST_NAME. Return its uri and id as a tuple."""
    response = spotify.user_playlist_create(user_id, playlist_name)
    return response['uri'], response['id']


def _add_tracks_to_playlist(user_id, playlist_id, tracks, spotify):
    """Add tracks to a playlist."""
    spotify.user_playlist_add_tracks(user_id, playlist_id, [track.id for track in tracks])


class SpotifyGateway:
    """Class implementing spotify gateway."""

    def __init__(self, access_token):
        """C'tor"""
        self._spotify = Spotify(access_token)


    def fetch_playlist_tracks(self, playlist_uri):
        """Fetch the tracks of a playlist as a list of Track namedtuples."""
        return SpotifyGateway._fetch_playlist_tracks(playlist_uri, self._spotify)


    def fetch_playlist_name(self, playlist_uri):
        """Fetch the name of a playlist from spotify."""
        return SpotifyGateway._fetch_playlist_name(playlist_uri, self._spotify)


    def fetch_collection_tracks(self, collection_id, collection_type):
        """Get a list of of Track namedtuples in a spotify collection.

        Args:
            collection_id: Id of the collection
            collection_type: Type of the collection ('artist' or 'album')

        Returns:
            Set of Track namedtuples

        """
        return SpotifyGateway._fetch_collection_tracks(
            collection_id,
            collection_type,
            self._spotify
        )


    def create_playlist_with_tracks(self, user_id, playlist_name, tracks):
        """Create a new playlist for USER_ID with TRACKS. Return the uri of the new playlist."""
        return SpotifyGateway._create_playlist_with_tracks(
            user_id,
            playlist_name,
            tracks,
            self._spotify
        )


    @staticmethod
    def _fetch_playlist_tracks(playlist_uri, spotify):
        """Fetch the tracks of a playlist as a list of Track namedtuples."""
        playlist_owner_id, playlist_id = _extract_playlist_uri_components(playlist_uri)
        playlist_track_data = _fetch_playlist_track_data(playlist_owner_id, playlist_id, spotify)
        return _pluck_tracks_as_list(playlist_track_data)


    @staticmethod
    def _fetch_playlist_name(playlist_uri, spotify):
        """Fetch the name of a playlist from spotify."""
        playlist_owner_id, playlist_id = _extract_playlist_uri_components(playlist_uri)
        return spotify.user_playlist(playlist_owner_id, playlist_id, fields='name')['name']


    @staticmethod
    def _fetch_collection_tracks(collection_id, collection_type, spotify):
        """Get a list of of Track namedtuples in a spotify collection."""
        if collection_type == 'artist':
            track_data = spotify.artist_top_tracks(collection_id)['tracks']
            tracks = _pluck_tracks_as_set(track_data, artist=collection_id)

        elif collection_type == 'album':
            track_data = spotify.album_tracks(collection_id)['items']
            tracks = _pluck_tracks_as_set(track_data, album=collection_id)

        else:
            raise SouffleParameterError('Invalid shuffle_by type "{}".'.format(collection_type))

        return tracks


    @staticmethod
    def _create_playlist_with_tracks(user_id, playlist_name, tracks, spotify):
        """Create a new playlist for USER_ID with TRACKS. Return the uri & id of the new playlist"""
        playlist_uri, playlist_id = _create_playlist(user_id, playlist_name, spotify)
        _add_tracks_to_playlist(user_id, playlist_id, tracks, spotify)
        return playlist_uri
