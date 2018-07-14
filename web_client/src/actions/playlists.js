import { getAccessToken } from 'selectors';
import { deletePlaylist } from 'services/api';

export const FETCH_PLAYLISTS_STARTED = 'FETCH_PLAYLISTS_STARTED';
export const FETCH_PLAYLISTS_SUCCEEDED = 'FETCH_PLAYLISTS_SUCCEEDED';
export const FETCH_PLAYLIST_STARTED = 'FETCH_PLAYLIST_STARTED';
export const FETCH_PLAYLIST_SUCCEEDED = 'FETCH_PLAYLIST_SUCCEEDED';
export const DELETE_PLAYLIST_STARTED = 'DELETE_PLAYLIST_STARTED';
export const DELETE_PLAYLIST_SUCCEEDED = 'DELETE_PLAYLIST_SUCCEEDED';

export const fetchPlaylistsSucceeded = (playlists) => ({
  type: FETCH_PLAYLISTS_SUCCEEDED,
  payload: {
    playlists
  }
});

export const fetchPlaylistsStarted = () => ({
  type: FETCH_PLAYLISTS_STARTED
});

export const fetchPlaylistSucceeded = (playlist) => ({
  type: FETCH_PLAYLIST_SUCCEEDED,
  payload: {
    playlist
  }
});

export const fetchPlaylistStarted = () => ({
  type: FETCH_PLAYLIST_STARTED
});

export const deletePlaylistSucceeded = (playlist) => ({
  type: DELETE_PLAYLIST_SUCCEEDED,
  payload: {
    playlist
  }
});

export const deletePlaylistStarted = () => ({
  type: DELETE_PLAYLIST_STARTED
});


export const handlePlaylistDeleted = playlist => (dispatch, getState) => {
  const state = getState();
  const accessToken = getAccessToken(state);
  dispatch(deletePlaylistStarted());
  dispatch(deletePlaylistSucceeded());
  // Not sure what to do if api delete playlist fails. Probably display a message to the user.
  deletePlaylist(accessToken, playlist)
    .catch(err => console.log(err));

};
