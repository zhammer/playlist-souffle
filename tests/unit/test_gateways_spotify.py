"""Unit test module for playlist_souffle.gateways.spotify."""

import pytest
from unittest.mock import Mock
import spotipy
from playlist_souffle.definitions.exception import SouffleSpotifyError
from playlist_souffle.definitions.track import Track
from playlist_souffle.gateways.spotify import SpotifyGateway

from playlist_souffle.gateways.spotify_util import (
    pluck_track,
    fetch_playlist_track_data,
    raise_spotipy_error_as_souffle_error
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
        track_data = fetch_playlist_track_data(spotify_mock, user_id, playlist_id)

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


class TestRaiseSpotipyErrorAsSouffleError:
    """Tests for decorator playlist_souffle.gateways.spotify_util.raise_spotify_error_as_souffle_error."""

    def test_function_that_returns_and_doesnt_raise(self):
        """Test a function that returns a value and doesnt raise an exception. Behavior should be
        unaltered.
        """
        # Given
        @raise_spotipy_error_as_souffle_error
        def func():
            return 1337

        # When / Then
        assert func() == 1337


    def test_function_that_doesnt_return_and_doesnt_raise(self):
        """Test a function that doesnt return a value and doesnt raise an exception. Behavior should
        be unaltered.
        """
        # Given
        @raise_spotipy_error_as_souffle_error
        def func():
            pass

        # When / Then
        assert func() == None


    def test_function_that_raises_runtime_errro(self):
        """Test a function that raises a runtime error. Runtime error raise should be unmodified."""
        # Given
        @raise_spotipy_error_as_souffle_error
        def func():
            raise RuntimeError

        # When / Then
        with pytest.raises(RuntimeError):
            func()


    def test_function_that_doesnt_return_and_doesnt_raise(self):
        """Test a function that doesnt return a value and doesnt raise an exception. Behavior should
        be unaltered.
        """
        @raise_spotipy_error_as_souffle_error
        def func():
            pass

        assert func() == None


    def test_function_that_raises_spotipy_error(self):
        """Test a function that returns a value and doesnt raise an exception. Behavior should be
        unaltered.
        """
        # Given
        http_status = 401
        message = "Unauthorized"
        @raise_spotipy_error_as_souffle_error
        def func():
            raise spotipy.SpotifyException(http_status=http_status, code=-1, msg=message)


        # When
        expected = SouffleSpotifyError(http_status=http_status, message=message)
        with pytest.raises(SouffleSpotifyError) as e:
            func()

        # Then
        assert e.value == expected


class TestFetchCollectionTracksByCollectionTrack:
    """Tests for playlist_souffle.gateways.fetch_collection_tracks_by_track."""

    def test_one_collection(self, blood_bank_ep):
        """Test fetch_collection_tracks_by_track with one collection to fetch."""
        # Given
        blood_bank_ep_id = 'BLOOD_BANK_EP_ID'
        blood_bank_ep_track_1 = blood_bank_ep[0]
        collection_id_by_track = {blood_bank_ep_track_1: blood_bank_ep_id}
        collection_type = 'ALBUM'
        spotify_gateway_mock = Mock()
        spotify_gateway_mock.fetch_collection_tracks.return_value = set(blood_bank_ep)

        # When
        collection_tracks_by_track = SpotifyGateway.fetch_collection_tracks_by_track(
            spotify_gateway_mock,
            collection_id_by_track,
            collection_type
        )

        # Then
        expected_collection_tracks_by_track = {
            blood_bank_ep_track_1: set(blood_bank_ep)
        }
        assert collection_tracks_by_track == expected_collection_tracks_by_track

    def test_two_collections(self, blood_bank_ep, soultrane):
        """Test fetch_collection_tracks_by_track with two collections to fetch."""
        # Given
        blood_bank_ep_id = 'BLOOD_BANK_EP_ID'
        soultrane_id = 'SOULTRANE_ID'
        blood_bank_ep_track_1 = blood_bank_ep[0]
        soultrane_track_1 = soultrane[0]
        collection_id_by_track = {
            blood_bank_ep_track_1: blood_bank_ep_id,
            soultrane_track_1: soultrane_id
        }
        collection_type = 'ALBUM'
        spotify_gateway_mock = Mock()
        def side_effect(collection_id, collection_type):
            return set(soultrane if collection_id == soultrane_id else blood_bank_ep)
        spotify_gateway_mock.fetch_collection_tracks.side_effect = side_effect

        # When
        collection_tracks_by_track = SpotifyGateway.fetch_collection_tracks_by_track(
            spotify_gateway_mock,
            collection_id_by_track,
            collection_type
        )

        # Then
        expected_collection_tracks_by_track = {
            blood_bank_ep_track_1: set(blood_bank_ep),
            soultrane_track_1: set(soultrane)
        }
        assert collection_tracks_by_track == expected_collection_tracks_by_track




@pytest.fixture()
def blood_bank_ep():
    """Blood Bank EP by Bon Iver"""
    track_names = ['Blood Bank', 'Beach Baby', 'Babys', 'Woods']
    return [Track(id=track_name, artist='Bon Iver', album='Blood Bank EP')
            for track_name in track_names]

@pytest.fixture()
def soultrane():
    """Soultrane by John Coltrane"""
    track_names = ['Good Bait',
                   'I Want To Talk About You',
                   'You Say You Care',
                   'Theme For Ernie',
                   'Russian Lullaby']
    return [Track(id=track_name, artist='Bon Iver', album='Blood Bank EP')
            for track_name in track_names]


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
