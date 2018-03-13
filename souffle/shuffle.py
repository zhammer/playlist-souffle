"""Module for shuffling spotify playlists"""

from collections import namedtuple
import logging
import random
import re
from souffle.exception import SouffleParameterError

SPOTIFY_PLAYLIST_FIELDS = 'items(track(id, artists.id, album.id))'
SOUFFLE_NAME_RE = r'(.*)\[souffle(?:\^(\d+))?\]$'
SOUFFLE_NAME_NO_DEGREE_FMT = '{} [souffle]'
SOUFFLE_NAME_DEGREE_FMT = '{} [souffle^{}]'

logger = logging.getLogger(__name__)

###################
# Track functions #
###################

Track = namedtuple('Track', 'id artist album')

def extract_track(track_record, artist=None, album=None):
    """Extract a Track namedtuple from a spotify api track object.
    Artist and album default values may be provided, in which case those field's data will not be
    extracted from the provided track data.

    Note: If there are multiple artists on a track, the track will only contain the id of the first
    artist listed.

    """
    return Track(
        id=track_record['id'],
        artist=(artist or track_record['artists'][0]['id']),
        album=(album or track_record['album']['id'])
    )


def extract_tracks_as_list(track_records, artist=None, album=None):
    """Extract list of Track namedtuples from a list of spotify api track objects.
    Artist and album default values may be provided, in which case those field's data will not be
    extracted from the provided track data.

    Note: If there are multiple artists on a track, the track will only contain the id of the first
    artist listed.

    """
    return [extract_track(track_record, artist, album) for track_record in track_records]


def extract_tracks_as_set(track_records, artist=None, album=None):
    """Extract list of Track namedtuples from a list of spotify api track objects.
    Artist and album default values may be provided, in which case those field's data will not be
    extracted from the provided track data.

    Note: If there are multiple artists on a track, the track will only contain the id of the first
    artist listed.

    """
    return {extract_track(track_record, artist, album) for track_record in track_records}


######################
# Playlist functions #
######################

def extract_playlist_uri_components(playlist_uri):
    """Extract, from a playlist uri ("spotify:user:{user}:playlist:{id}"), the user and id fields.
    Raises a SouffleParameterError if playlist uri isn't correctly formatted.

    """
    components = playlist_uri.split(':')
    try:
        return components[2], components[4]
    except IndexError:
        raise SouffleParameterError('Invalid playlist uri: "{}"'.format(playlist_uri))


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


def fetch_playlist_tracks(playlist_uri, spotify):
    """Fetch the tracks of a playlist as a list of Track namedtuples.

    Args:
        playlist_uri: String uri of playlist to be fetched. "spotify:user:{user}:playlist:{id}"
        spotify: Spotify client

    Returns:
        List of Track namedtuples

    Raises:
        - SpotifyException if request to fetch playlists fails

    """

    user_id, playlist_id = extract_playlist_uri_components(playlist_uri)
    playlist_track_data = fetch_playlist_track_data(user_id, playlist_id, spotify)
    playlist_tracks = extract_tracks_as_list(playlist_track_data)

    return playlist_tracks


def fetch_playlist_name(playlist_uri, spotify):
    """Fetch the name of a playlist from spotify."""
    user_id, playlist_id = extract_playlist_uri_components(playlist_uri)
    return spotify.user_playlist(user_id, playlist_id, fields='name')['name']



#####################
# Shuffle functions #
#####################

def fetch_collection_tracks(collection_id, collection_type, spotify):
    """Get a list of of Track namedtuples in a spotify collection.

    Args:
        collection_id: Id of the collection
        collection_type: Type of the collection ('artist' or 'album')
        spotify: Spotify client

    Returns:
        Set of Track namedtuples

    Raises:
        SpotifyException if fetch request to spotify fails

    """
    if collection_type == 'artist':
        track_data = spotify.artist_top_tracks(collection_id)['tracks']
        tracks = extract_tracks_as_set(track_data, artist=collection_id)

    elif collection_type == 'album':
        track_data = spotify.album_tracks(collection_id)['items']
        tracks = extract_tracks_as_set(track_data, album=collection_id)

    else:
        raise SouffleParameterError('Invalid shuffle_by type "{}".'.format(collection_type))

    return tracks


def remove_tracks_from_collections(collections_map, tracks_to_remove, collection_type):
    """From a dictionary mapping collection ids to tracks in the collection, remove all tracks
    in tracks_to_remove from the collection to which the track belongs.

    Notes:
    - this is a helper function for shuffle_tracks, and it is assumed that each track
    belongs to one of the collection ids in the collection_map. separated for testing.

    Args:
        collections_map: Dictionary mapping collection ids to Track namedtuples
        tracks_to_remove: List of Track namedtuples
        collection_type: Type of collection: 'artist' or 'album'

    Returns:
        Dictionary mapping collection ids to Track namedtuples

    Side effects:
        collections_map is filtered as-is rather than copied for the sake of efficiency

    """
    for track in tracks_to_remove:
        collection_id = track._asdict()[collection_type]
        collection_tracks = collections_map[collection_id]
        try:
            collection_tracks.remove(track)
        except KeyError:
            pass

    return collections_map


def shuffle_tracks(tracks, shuffle_by, spotify):
    """Shuffle a list of Track namedtuples by artist or album, in which each track is shuffled
    out with another track on that track's artist or album. If there are no other tracks on a
    track's collection, the track will not be shuffled. Two tracks by the same artist or on
    the same album will not be shuffled to each other, nor will they be shuffled to the same other
    track in that collection. Thus, in the case that a playlist contains all of the tracks on an
    album, and the tracks are requested to be shuffled by album, no track will be shuffled, as there
    is nothing to shuffle to that doesn't exist on the playlist already.

    Args:
        tracks: List of Track namedtuples
        shuffle_by: What collection the track should be shuffled by: 'artist' or 'album'
        spotify: Spotify client

    Returns:
        A list of track ids of the shuffled tracks

    Raises:
        - SpotifyException if an error occurs with the spotify client

    """
    try:
        collection_ids = {track._asdict()[shuffle_by] for track in tracks}
    except KeyError:
        raise SouffleParameterError('Invalid shuffle_by type "{}".'.format(shuffle_by))

    # For each collection (album or arist) get all of the tracks on that collection
    collection_to_tracks_map = {}
    for collection_id in collection_ids:
        collection_to_tracks_map[collection_id] = fetch_collection_tracks(
            collection_id=collection_id,
            collection_type=shuffle_by,
            spotify=spotify
        )

    # Remove all original tracks from the collections to tracks map to avoid
    collection_to_tracks_map = remove_tracks_from_collections(
        collections_map=collection_to_tracks_map,
        tracks_to_remove=tracks,
        collection_type=shuffle_by
    )

    # Shuffle each track
    shuffled_tracks = []
    for track in tracks:
        collection_id = track._asdict()[shuffle_by]
        collection_tracks = collection_to_tracks_map[collection_id]

        # Nothing to shuffle with
        if not collection_tracks:
            shuffled_tracks.append(track)

        # Otherwise, shuffle track with another track in the collection. Remove the
        # track from the collection afterwards to avoid duplication.
        else:
            shuffled_track = random.sample(collection_tracks, k=1)[0]
            shuffled_tracks.append(shuffled_track)
            collection_tracks.remove(shuffled_track)

    return shuffled_tracks


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

    # Playlist name doesn't end in '[souffle]'. Append souffle to end of name and return.
    if not match:
        return SOUFFLE_NAME_NO_DEGREE_FMT.format(original_name.rstrip())

    # Playlist name ends in '[souffle(^\d+)?]. Increment the souffle degree.
    playlist_name = match.group(1).rstrip()

    # Extract the souffle degree if it exists, if it doesn't set to 1.
    try:
        souffle_degree = int(match.group(2))
    except TypeError:
        souffle_degree = 1

    return SOUFFLE_NAME_DEGREE_FMT.format(playlist_name, souffle_degree + 1)


def souffle_playlist(playlist_uri, shuffle_by, user_id, spotify, destination_uri=None):
    """Souffle"""
    logger.info(
        'souffle: playlist_uri: "%s", shuffle_by: "%s", user_id: "%s", destination_uri: "%s"',
        playlist_uri,
        shuffle_by,
        user_id,
        destination_uri
    )

    playlist_name = fetch_playlist_name(playlist_uri, spotify)
    playlist_tracks = fetch_playlist_tracks(playlist_uri, spotify)

    shuffled_tracks = shuffle_tracks(playlist_tracks, shuffle_by, spotify)

    # If this is not a resouffle request, generate a souffle name and create a new playlist.
    if not destination_uri:
        destination_name = generate_souffle_name(playlist_name)
        response = spotify.user_playlist_create(user_id, destination_name)
        destination_uri = response['uri']
        destination_id = response['id']

    # Otherwise, clear the existing playlist to repopulate with the resouffled tracks.
    else:
        raise NotImplemented('Souffleing a playlist in-place (resouffle) NYI.')
        # TODO: get id from destination
        # TODO: remove tracks from original playlist

    track_ids = [track.id for track in shuffled_tracks]
    spotify.user_playlist_add_tracks(user_id, destination_id, track_ids)

    return destination_uri
