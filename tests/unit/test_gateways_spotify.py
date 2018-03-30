"""Unit test module for playlist_souffle.gateways.spotify."""

import pytest
from unittest.mock import Mock
from playlist_souffle.definitions.track import Track
from playlist_souffle.gateways.spotify_util import (
    pluck_track,
    fetch_playlist_track_data,
    create_playlist
)

class TestSpotifyUtil:
    """Tests for playlist_souffle.gateways.spotify_util functions."""

    def test_fetch_playlist_track_data(self, spotify_playlist_tracks_response):
        """Simple test to make sure fetch_playlist_track_data properly extracks track data from
        a spotify playlist tracks response."""
        # Given
        spotify_mock = Mock()
        spotify_mock.user_playlist_tracks = Mock(return_value=spotify_playlist_tracks_response)
        user_id = ''
        playlist_id = ''

        # When
        track_data = fetch_playlist_track_data(user_id, playlist_id, spotify_mock)

        # Then
        expected_track_1 = {'album': {'id': 'ALBUM_ID_1'},
                            'artists': [{'id': 'ARTIST_ID_1'}],
                            'id': 'TRACK_ID_1'}
        expected_track_2 = {'album': {'id': 'ALBUM_ID_2'},
                            'artists': [{'id': 'ARTIST_ID_2'}],
                            'id': 'TRACK_ID_2'}
        expected_track_3 = {'album': {'id': 'ALBUM_ID_3'},
                            'artists': [{'id': 'ARTIST_ID_3'}],
                            'id': 'TRACK_ID_3'}
        expected_tracks = [expected_track_1, expected_track_2, expected_track_3]
        assert len(track_data) == 3
        assert all([expected_track in track_data for expected_track in expected_tracks])


    def test_pluck_track_simple(self, spotify_track_object):
        """Simple test case for plucking a Track namedtuple from a spotify track object."""
        # Given / When
        plucked_track = pluck_track(spotify_track_object)

        # Then
        expected_track = Track('TRACK_ID', 'ARTIST_ID', 'ALBUM_ID')
        assert plucked_track == expected_track


    def test_pluck_track_provide_artist(self, spotify_track_object):
        """Provide an 'artist' field when plucking a track."""
        # Given / When
        custom_artist = 'CUSTOM_ARTIST'
        plucked_track = pluck_track(spotify_track_object, artist=custom_artist)

        # Then
        expected_track = Track('TRACK_ID', custom_artist, 'ALBUM_ID')
        assert plucked_track == expected_track


    def test_pluck_track_provide_album(self, spotify_track_object):
        """Provide an 'album' field when plucking a track."""
        # Given / When
        custom_album = 'CUSTOM_ALBUM'
        plucked_track = pluck_track(spotify_track_object, album=custom_album)

        # Then
        expected_track = Track('TRACK_ID', 'ARTIST_ID', custom_album)
        assert plucked_track == expected_track

    def test_pluck_track_with_two_albums(self, spotify_track_object_two_artists):
        """Pluck a track with two artists. Only the first artist should be plucked."""
        # Given / When
        plucked_track = pluck_track(spotify_track_object_two_artists)

        # Then
        expected_track = Track('TRACK_ID', 'ARTIST_ID_1', 'ALBUM_ID')
        assert plucked_track == expected_track


@pytest.fixture()
def spotify_track_object():
    """Data fixture for a spotify playlist track object."""
    return {
        'album': {'id': 'ALBUM_ID'},
        'artists': [{'id': 'ARTIST_ID'}],
        'id': 'TRACK_ID'
    }

@pytest.fixture()
def spotify_track_object_two_artists():
    """Data fixture for a spotify playlist track object."""
    return {
        'album': {'id': 'ALBUM_ID'},
        'artists': [{'id': 'ARTIST_ID_1'},
                    {'id': 'ARTIST_ID_2'}],
        'id': 'TRACK_ID'
    }

@pytest.fixture()
def spotify_playlist_tracks_response():
    """Data fixture for spotify playlist tracks response."""
    return {
        'items': [
            {
                'track': {
                    'album': {
                        'id': 'ALBUM_ID_1'
                    },
                    'artists': [
                        {
                            'id': 'ARTIST_ID_1'
                        }
                    ],
                    'id': 'TRACK_ID_1'
                }
            },
            {
                'track': {
                    'album': {
                        'id': 'ALBUM_ID_2'
                    },
                    'artists': [
                        {
                            'id': 'ARTIST_ID_2'
                        }
                    ],
                    'id': 'TRACK_ID_2'
                }
            },
            {
                'track': {
                    'album': {
                        'id': 'ALBUM_ID_3'
                    },
                    'artists': [
                        {
                            'id': 'ARTIST_ID_3'
                        }
                    ],
                    'id': 'TRACK_ID_3'
                }
            },

        ]
    }
