import { push } from 'connected-react-router';
import {
  fetchAccessTokenSucceeded,
  fetchRefreshTokenSucceeded,
  fetchAccessTokenStarted,
  fetchRefreshTokenStarted,
  handleAuthCodeReceived,
} from 'actions/auth';
import {
  fetchPlaylistsStarted,
  fetchPlaylistsSucceeded
} from 'actions/playlists';
import { getAuthCode } from 'selectors';
import { fetchAccessToken, fetchPlaylists } from 'services/api';

export const handleApplicationStarted = () => (dispatch, getState) => {
  const refreshToken = localStorage.getItem('refreshToken');
  const authCode = getAuthCode(getState());

  if (!refreshToken) {
    if (authCode) {
      dispatch(handleAuthCodeReceived(authCode));
      return;
    }
    else {
      dispatch(push('/'));
      return;
    }
  }

  dispatch(fetchAccessTokenStarted());
  dispatch(fetchRefreshTokenStarted());

  fetchAccessToken(refreshToken)
    .then(accessToken => {
      // See note in auth.handleAuthCodeReceived!!
      dispatch(fetchPlaylistsStarted());
      dispatch(fetchAccessTokenSucceeded(accessToken));
      dispatch(fetchRefreshTokenSucceeded(refreshToken));

      fetchPlaylists(accessToken)
        .then(playlists => dispatch(fetchPlaylistsSucceeded(playlists)))
        .catch(err => alert(err));
    })
    .catch(error => localStorage.removeItem('refreshToken'));
};
