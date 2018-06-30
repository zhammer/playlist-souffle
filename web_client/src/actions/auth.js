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
  console.log(authCode);
  fetchRefreshToken(authCode)
    .then(({ refreshToken, accessToken }) => dispatch(fetchRefreshTokenSucceeded(refreshToken, accessToken)))
    .catch(error => alert(error));
};
