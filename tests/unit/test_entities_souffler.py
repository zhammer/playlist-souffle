"""Unit test module for playlist_souffle.entities.souffler."""

import pytest
from playlist_souffle.definitions.track import Track
from playlist_souffle.entities.souffler import (
    generate_souffle_name,
    souffle_tracks
)

class TestSouffleTracks:
    """Tests for playlist_souffle.entities.souffler.souffle_tracks"""

    def test_empty_input(self):
        """Empty input parameters. Should return an empty list."""
        # Given / When
        souffled_tracks = souffle_tracks([], {})

        # Then
        assert souffled_tracks == []

    def test_one_track_collection_size_one(self, dummy_track):
        """One track in 'tracks', where the track's collection has only the track itself.
        Should return a list with one track which is the input track.
        """
        # Given
        tracks = [dummy_track]
        track_collections = {dummy_track: {dummy_track}}

        # When
        souffled_tracks = souffle_tracks(tracks, track_collections)

        # Then
        assert len(souffled_tracks) == 1
        assert souffled_tracks == tracks

    def test_souffle_album(self, blood_bank_ep):
        """Souffle the tracks of an album, where each track's collection is the album itself.
        The souffled playlist tracks should include all the tracks in the album.
        """
        # Given
        tracks = blood_bank_ep
        track_collections = {track: set(blood_bank_ep) for track in tracks}

        # When
        souffled_tracks = souffle_tracks(tracks, track_collections)

        # Then
        assert len(souffled_tracks) == len(tracks)
        assert all(souffled_track in tracks for souffled_track in souffled_tracks)

    def test_two_tracks_different_collections(self, blood_bank_ep, soultrane):
        """Souffle two tracks from different collections, that both can be swapped to other tracks
        on their respective collections."""
        # Given
        blood_bank_ep_track = blood_bank_ep[0]
        soultrane_track = soultrane[0]
        tracks = [blood_bank_ep_track, soultrane_track]
        track_collections = {
            blood_bank_ep_track: set(blood_bank_ep),
            soultrane_track: set(soultrane)
        }

        # When
        souffled_tracks = souffle_tracks(tracks, track_collections)

        # Then
        assert len(souffled_tracks) == len(tracks)

        blood_bank_ep_track_souffled = souffled_tracks[0]
        soultrane_track_souffled = souffled_tracks[1]
        assert (blood_bank_ep_track in blood_bank_ep
                and blood_bank_ep_track_souffled is not blood_bank_ep_track)
        assert (soultrane_track in soultrane
                and soultrane_track_souffled is not soultrane_track)

    def test_two_tracks_same_collection(self, blood_bank_ep):
        """Souffle two tracks from the same collection that both can be swapped to other tracks
        on the collection."""
        # Given
        tracks = blood_bank_ep[:2]
        track_collections = {track: set(blood_bank_ep) for track in tracks}

        # When
        souffled_tracks = souffle_tracks(tracks, track_collections)

        # Then
        assert len(souffled_tracks) == len(tracks)

        assert all([souffled_track in blood_bank_ep
                   for souffled_track in souffled_tracks])
        assert all([souffled_track not in tracks
                   for souffled_track in souffled_tracks])
        assert not souffled_tracks[0] == souffled_tracks[1]


@pytest.fixture()
def dummy_track():
    """A simple track."""
    return Track(id='TRACK_ID', artist='ARTIST_ID', album='ALBUM_ID')

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
