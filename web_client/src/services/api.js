import request from 'superagent';

const CLIENT_ID = 'b231329aba1a4c539375436a267db917';
//const REDIRECT_URI = 'http://127.0.0.1:3000';
const REDIRECT_URI = 'http://192.168.1.151:3000';

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

export async function souffle (accessToken, playlistUri, souffleBy) {
  const response = await request.post(BASE_URL + '/souffle')
        .set('Authorization', 'Bearer ' + accessToken)
        .send({ playlistUri })
        .send({ shuffleBy: souffleBy })
        .type('form');

  if (response.status !== 201) {
    throw response.body;
  }

  return response.headers['location'];
}


const SPOTIFY_URL = 'https://api.spotify.com/v1';

export async function fetchPlaylists (accessToken) {
  const response = await request.get(SPOTIFY_URL + '/me/playlists?limit=50')
        .set('Authorization', 'Bearer ' + accessToken);

  return response.body.items.map(
    ({ id, name, uri }) => ({
      id,
      name,
      uri
    })
  );
}

export const playlistPathFromUri = playlistUri => {
  const substrings = playlistUri.split(':');
  const user = substrings[2];
  const playlist = substrings[4];
  return '/users/' + user + '/playlists/' + playlist;
};

export async function fetchPlaylist (accessToken, playlistUri) {
  const playlistPath = playlistPathFromUri(playlistUri);
  const response = await request.get(SPOTIFY_URL + playlistPath)
        .set('Authorization', 'Bearer ' + accessToken)
        .query({ fields: 'name,id,uri' });

  return response.body;

}

export async function deletePlaylist (accessToken, { uri }) {
  const playlistPath = playlistPathFromUri(uri);
  const response = await request.delete(SPOTIFY_URL + playlistPath + '/followers')
        .set('Authorization', 'Bearer ' + accessToken);

  return response;
}
