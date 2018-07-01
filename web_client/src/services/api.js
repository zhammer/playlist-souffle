import request from 'superagent';

const CLIENT_ID = 'b231329aba1a4c539375436a267db917';
const REDIRECT_URI = 'http://127.0.0.1:3000';

export const redirectToAuthorizationPage = () => {
  window.location = 'https://accounts.spotify.com/authorize?client_id=' + CLIENT_ID
    + '&response_type=code&redirect_uri=' + REDIRECT_URI
    + '&scope=playlist-read-private%20playlist-modify-private%20playlist-modify-public';
};


const BASE_URL = '';

export async function fetchRefreshToken (authCode) {
  const body = 'redirectUri=' + REDIRECT_URI;

  const response = await request.post(BASE_URL + '/refreshtoken')
        .set('Authorization', 'Bearer ' + authCode)
        .send(body);

  if (response.status !== 200) {
    throw response.body;
  }

  const { body: { refreshToken, accessToken }} = response;
  return { refreshToken, accessToken };
}

export async function fetchAccessToken (refreshToken) {

  const response = await request.post(BASE_URL + '/accesstoken')
        .set('Authorization', 'Bearer ' + refreshToken);

  if (response.status !== 200) {
    throw response.body;
  }

  return response.body.accessToken;
}


const SPOTIFY_URL = 'https://api.spotify.com/v1';

export async function fetchPlaylists (accessToken) {
  const response = await request.get(SPOTIFY_URL + '/me/playlists')
        .set('Authorization', 'Bearer ' + accessToken);

  return response.body;
}
