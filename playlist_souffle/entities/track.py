"""Module for the track entity."""


def extract_track_collection_id(track, collection_type):
    """Extract the collection id of a track for the given collection_type.

    >>> from playlist_souffle.definitions.track import Track
    >>> my_track = Track(id='TRACK_ID', artist='ARTIST_ID', album='ALBUM_ID')

    >>> extract_track_collection_id(my_track, 'artist')
    'ARTIST_ID'

    >>> extract_track_collection_id(my_track, 'album')
    'ALBUM_ID'

    """
    return track._asdict()[collection_type]
