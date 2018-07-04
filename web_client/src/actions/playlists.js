export const FETCH_PLAYLISTS_STARTED = 'FETCH_PLAYLISTS_STARTED';
export const FETCH_PLAYLISTS_SUCCEEDED = 'FETCH_PLAYLISTS_SUCCEEDED';
export const FETCH_PLAYLIST_TRACKS_STARTED = 'FETCH_PLAYLIST_TRACKS_STARTED';
export const FETCH_PLAYLIST_TRACKS_SUCCEEDED = 'FETCH_PLAYLIST_TRACKS_SUCCEEDED';

export const fetchPlaylistsSucceeded = (playlists) => ({
  type: FETCH_PLAYLISTS_SUCCEEDED,
  payload: {
    playlists
  }
});

export const fetchPlaylistsStarted = () => ({
  type: FETCH_PLAYLISTS_STARTED
});

export const fetchPlaylistTracksStarted = () => ({
  type: FETCH_PLAYLIST_TRACKS_STARTED
});

export const fetchPlaylistTracksSucceeded = (playlistId, tracks) => ({
  type: FETCH_PLAYLIST_TRACKS_SUCCEEDED,
  payload: {
    playlistId,
    tracks
  }
});
