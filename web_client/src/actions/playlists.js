export const FETCH_PLAYLISTS_STARTED = 'FETCH_PLAYLISTS_STARTED';
export const FETCH_PLAYLISTS_SUCCEEDED = 'FETCH_PLAYLISTS_SUCCEEDED';

export const fetchPlaylistsSucceeded = (playlists) => ({
  type: FETCH_PLAYLISTS_SUCCEEDED,
  payload: {
    playlists
  }
});

export const fetchPlaylistsStarted = () => ({
  type: FETCH_PLAYLISTS_STARTED
});
