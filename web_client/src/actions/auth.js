import { fetchRefreshToken, fetchPlaylists } from 'services/api';
import {
  fetchPlaylistsStarted,
  fetchPlaylistsSucceeded
} from 'actions/playlists';

export const FETCH_REFRESH_TOKEN_SUCCEEDED = 'FETCH_REFRESH_TOKEN_SUCCEEDED';
export const FETCH_ACCESS_TOKEN_SUCCEEDED = 'FETCH_ACCESS_TOKEN_SUCCEEDED';
export const FETCH_REFRESH_TOKEN_STARTED = 'FETCH_REFRESH_TOKEN_STARTED';
export const FETCH_ACCESS_TOKEN_STARTED = 'FETCH_ACCESS_TOKEN_STARTED';

export const fetchRefreshTokenSucceeded = (refreshToken) => ({
  type: FETCH_REFRESH_TOKEN_SUCCEEDED,
  payload: {
    refreshToken
  }
});

export const fetchAccessTokenSucceeded = (accessToken) => ({
  type: FETCH_ACCESS_TOKEN_SUCCEEDED,
  payload: {
    accessToken
  }
});

export const fetchRefreshTokenStarted = () => ({
  type: FETCH_REFRESH_TOKEN_STARTED
});

export const fetchAccessTokenStarted = () => ({
  type: FETCH_ACCESS_TOKEN_STARTED
});




export const handleAuthCodeReceived = authCode => dispatch => {
  fetchRefreshToken(authCode)
    .then(({ refreshToken, accessToken }) => {
      localStorage.setItem('refreshToken', refreshToken);

      // NOTE: This is all repeat logic from handleApplicationStarted! Clean this up.
      dispatch(fetchPlaylistsStarted());
      dispatch(fetchAccessTokenSucceeded(accessToken));
      dispatch(fetchRefreshTokenSucceeded(refreshToken));

      fetchPlaylists(accessToken)
        .then(playlists => dispatch(fetchPlaylistsSucceeded(playlists)))
        .catch(err => alert(err));

    })
    .catch(error => alert(error));
};
