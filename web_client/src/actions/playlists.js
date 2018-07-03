import { fetchPlaylists } from 'services/api';
import { getAccessToken, getFetchingAccessToken } from 'selectors';

export const FETCH_PLAYLISTS_STARTED = 'FETCH_PLAYLISTS_STARTED';
export const FETCH_PLAYLISTS_SUCCEEDED = 'FETCH_PLAYLISTS_SUCCEEDED';

const fetchPlaylistsSucceeded = (playlists) => ({
  type: FETCH_PLAYLISTS_SUCCEEDED,
  payload: {
    playlists
  }
});

const fetchPlaylistsStarted = (playlists) => ({
  type: FETCH_PLAYLISTS_STARTED
});

export const handlePlaylistsPageLoaded = () => (dispatch, getState) => {
  const state = getState();
  const fetchingAccessToken = getFetchingAccessToken(state);

  // Note: This is a super hacky fix so that if a user loads the site at /playlists, the user's
  // playlists won't be fetched until the handleApplicationStarted thunk has fetched an access
  // token (if there is a refreshToken stored in localStorage). This also required that I set
  // fetchingAccessToken and fetchingRefreshToken to true as part of the auth reducer's initial
  // state.
  if (fetchingAccessToken) {
    setTimeout(() => dispatch(handlePlaylistsPageLoaded()), 100);
    return;
  }
  const accessToken = getAccessToken(state);

  dispatch(fetchPlaylistsStarted());
  fetchPlaylists(accessToken)
    .then(playlists => dispatch(fetchPlaylistsSucceeded(playlists)))
    .catch(err => console.log(err)); // Should clear accesstoken
};

export const handlePlaylistSelected = playlist => dispatch => {
  console.log(playlist);
};
