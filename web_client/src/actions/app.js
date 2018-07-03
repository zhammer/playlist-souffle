import { fetchAccessTokenSucceeded, fetchRefreshTokenSucceeded,
         fetchAccessTokenStarted, fetchRefreshTokenStarted
       } from 'actions/auth';
import { fetchAccessToken } from 'services/api';

export const handleApplicationStarted = () => dispatch => {
  const refreshToken = localStorage.getItem('refreshToken');

  if (!refreshToken) {
    return;
  }

  dispatch(fetchAccessTokenStarted());
  dispatch(fetchRefreshTokenStarted());

  fetchAccessToken(refreshToken)
    .then(accessToken => {
      dispatch(fetchAccessTokenSucceeded(accessToken));
      dispatch(fetchRefreshTokenSucceeded(refreshToken));
    })
    .catch(error => localStorage.removeItem('refreshToken'));
};
