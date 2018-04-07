"""Module for testing playlist_souffle.use_cases.souffle_playlist."""

from datetime import datetime as dt
from unittest.mock import Mock, patch
import pytest
from playlist_souffle.definitions.playlist import Playlist
from playlist_souffle.definitions.track import Track
from playlist_souffle.use_cases.souffle_playlist import souffle_playlist


class TestSoufflePlaylist:
    """Tests for souffle_playlist function."""

    def test_two_tracks_simple(self, art_tatum_tracks, the_xx_tracks):
        """Souffle a playlist with two tracks by artist. Each track's artist has 2 songs in their
        'top tracks', so each track should be souffled to the other track by the artist."""
        # Given
        playlist_uri = 'playlist uri'
        user_id = 'zhammer'

        playlist_name = '~coding~'

        art_tatum_track = art_tatum_tracks[0]
        the_xx_track = the_xx_tracks[0]
        playlist_tracks = [art_tatum_track, the_xx_track]

        injected_souffled_playlist_uri = 'SOUFFLED_PLAYLIST_URI'
        injected_dt =  dt(1968, 11, 22, hour=9, minute=30, second=15)

        spotify_mock = Mock()
        collection_tracks_by_track = {
            art_tatum_track: set(art_tatum_tracks),
            the_xx_track: set(the_xx_tracks)
        }
        spotify_mock.fetch_collection_tracks_by_track.return_value = collection_tracks_by_track
        spotify_mock.fetch_playlist_tracks.return_value = playlist_tracks
        spotify_mock.fetch_playlist_name.return_value = playlist_name
        spotify_mock.create_playlist.return_value = injected_souffled_playlist_uri

        # When
        with patch('playlist_souffle.use_cases.souffle_playlist.dt') as mock_dt:
            mock_dt.now.return_value = injected_dt
            souffled_playlist_uri = souffle_playlist(spotify_mock, playlist_uri, user_id, 'artist')

        # Then
        expected_playlist = Playlist(
            user_id=user_id,
            name='~coding~ [souffle]',
            tracks=[art_tatum_tracks[1], the_xx_tracks[1]],
            description='Souffled from "~coding~" by "artist" at 1968-11-22 09:30:15.'

        )
        assert souffled_playlist_uri == injected_souffled_playlist_uri
        spotify_mock.create_playlist.assert_called_once_with(
            expected_playlist
        )







@pytest.fixture()
def art_tatum_tracks():
    """Two tracks by art tatum"""
    track_names = ['Willow Weep For Me', 'Over the Rainbow']
    return [Track(id=track_name, artist='Art Tatum', album='N/A')
            for track_name in track_names]

@pytest.fixture()
def the_xx_tracks():
    """Two tracks by the xx"""
    track_names = ['VCR', 'Crystalised']
    return [Track(id=track_name, artist='The xx', album='N/A')
            for track_name in track_names]
