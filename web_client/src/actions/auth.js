import { fetchRefreshToken } from 'services/api';

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
      dispatch(fetchRefreshTokenSucceeded(refreshToken));
      dispatch(fetchAccessTokenSucceeded(accessToken));
      localStorage.setItem('refreshToken', refreshToken);
    })
    .catch(error => alert(error));
};
