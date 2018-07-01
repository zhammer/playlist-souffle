import { fetchRefreshToken } from 'services/api';

export const FETCH_REFRESH_TOKEN_SUCCEEDED = 'FETCH_REFRESH_TOKEN_SUCCEEDED';
export const FETCH_ACCESS_TOKEN_SUCCEEDED = 'FETCH_ACCESS_TOKEN_SUCCEEDED';

export const fetchRefreshTokenSucceeded = (refreshToken, accessToken) => ({
  type: FETCH_REFRESH_TOKEN_SUCCEEDED,
  payload: {
    refreshToken,
    accessToken
  }
});

export const fetchAccessTokenSucceeded = (accessToken) => ({
  type: FETCH_ACCESS_TOKEN_SUCCEEDED,
  payload: {
    accessToken
  }
});


export const handleAuthCodeReceived = authCode => dispatch => {
  fetchRefreshToken(authCode)
    .then(({ refreshToken, accessToken }) => {
      dispatch(fetchRefreshTokenSucceeded(refreshToken, accessToken));
      localStorage.setItem('refreshToken', refreshToken);
    })
    .catch(error => alert(error));
};
