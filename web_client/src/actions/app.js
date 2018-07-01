import { fetchRefreshTokenSucceeded } from 'actions/auth';
import { fetchAccessToken } from 'services/api';

export const handleApplicationStarted = () => dispatch => {
  const refreshToken = localStorage.getItem('refreshToken');

  if (!refreshToken) {
    return;
  }

  // Note: Shouldn't use fetchRefreshTokenSucceeded
  fetchAccessToken(refreshToken)
    .then(accessToken => dispatch(fetchRefreshTokenSucceeded(refreshToken, accessToken)))
    .catch(error => localStorage.removeItem('refreshToken'));
};
