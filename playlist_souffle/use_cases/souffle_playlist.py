"""Module for the souffle_playlist use case."""

from datetime import datetime as dt
from playlist_souffle.definitions.playlist import Playlist
import playlist_souffle.entities.souffler as souffler_entity
import playlist_souffle.entities.track as track_entity

def souffle_playlist(spotify, playlist_uri, user_id, shuffle_by):
    """Souffle a playlist."""

    playlist_name = spotify.fetch_playlist_name(playlist_uri)
    playlist_tracks = spotify.fetch_playlist_tracks(playlist_uri)

    collection_id_by_track = {track: track_entity.extract_track_collection_id(track, shuffle_by)
                              for track in playlist_tracks}

    collection_tracks_by_collection_id = spotify.fetch_collection_tracks_by_collection_id(
        collection_id_by_track.values(),
        collection_type=shuffle_by
    )

    collection_tracks_by_track = {track: collection_tracks_by_collection_id[collection_id_by_track[track]]
                                  for track in playlist_tracks}

    playlist = Playlist(
        owner=user_id,
        name=playlist_name,
        tracks=playlist_tracks,
        description=''
    )

    souffled_playlist = souffler_entity.generate_souffled_playlist(
        playlist,
        shuffle_by,
        collection_tracks_by_track,
        dt.now()
    )

    souffled_playlist_uri = spotify.create_playlist(souffled_playlist)

    return souffled_playlist_uri
