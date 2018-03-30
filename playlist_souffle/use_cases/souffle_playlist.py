"""Module for the souffle_playlist use case."""

from datetime import datetime as dt
import playlist_souffle.entities.souffler as souffler_entity
import playlist_souffle.entities.track as track_entity

def souffle_playlist(spotify, playlist_uri, user_id, shuffle_by):
    """Souffle a playlist."""

    playlist_tracks = spotify.fetch_playlist_tracks(playlist_uri)

    playlist_track_collection_ids = {track: track_entity.extract_track_collection_id(track, shuffle_by)
                                     for track in playlist_tracks}

    playlist_track_collections = {track: spotify.fetch_collection_tracks(collection_id, shuffle_by)
                                  for track, collection_id in playlist_track_collection_ids.items()}

    souffled_playlist_tracks = souffler_entity.souffle_tracks(
        playlist_tracks,
        playlist_track_collections
    )

    playlist_name = spotify.fetch_playlist_name(playlist_uri)

    souffled_playlist_name = souffler_entity.generate_souffle_name(playlist_name)
    souffled_playlist_description = souffler_entity.generate_souffle_description(
        playlist_name,
        shuffle_by,
        dt.now()
    )

    souffled_playlist_uri = spotify.create_playlist_with_tracks(
        user_id,
        souffled_playlist_name,
        souffled_playlist_tracks,
        description=souffled_playlist_description
    )

    return souffled_playlist_uri
