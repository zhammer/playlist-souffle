"""Module for the souffle_playlist use case."""

from datetime import datetime as dt
from playlist_souffle.definitions.playlist import Playlist
import playlist_souffle.entities.souffler as souffler_entity
import playlist_souffle.entities.track as track_entity

def souffle_playlist(spotify, playlist_uri, user_id, shuffle_by):
    """Souffle a playlist."""

    original_playlist = Playlist(
        owner=None,
        name=spotify.fetch_playlist_name(playlist_uri),
        tracks=spotify.fetch_playlist_tracks(playlist_uri),
        description=None
    )

    collection_id_by_track = {track: track_entity.extract_track_collection_id(track, shuffle_by)
                              for track in original_playlist.tracks}

    collection_tracks_by_track = spotify.fetch_collection_tracks_by_track(
        collection_id_by_track,
        collection_type=shuffle_by
    )

    souffled_playlist = souffler_entity.generate_souffled_playlist(
        original_playlist,
        user_id,
        shuffle_by,
        collection_tracks_by_track,
        souffle_time=dt.now()
    )

    souffled_playlist_uri = spotify.create_playlist(souffled_playlist)

    return souffled_playlist_uri
