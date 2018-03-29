"""Module for the track entity."""


def extract_track_collection_id(track, collection_type):
    """Extract the collection id of a track for the given collection_type. For example, if
    collection_type is 'artist', return the id of the track's artist.
    """
    return track._asdict()[collection_type]
