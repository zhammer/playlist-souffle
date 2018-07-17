import request from 'superagent';

const REDIRECT_URI = 'https://playlistsouffle.com';

// --------------------
// Playlist Souffle API
// --------------------

const BASE = 'https://api.playlistsouffle.com';

/**
 *  Fetch a spotify accessToken (used for temporary access to the Spotify API) and a refreshToken
 *  (used for long-term ability to obtain fresh accessTokens) for the current user, given a spotify
 *  authCode obtained via the spotify authorization page.
 */
export async function fetchRefreshToken (authCode) {
  const response = await request.post(BASE + '/refreshtoken')
        .set('Authorization', 'Bearer ' + authCode)
        .send({ redirectUri: REDIRECT_URI });

  if (response.status !== 200) {
    throw response.body;
  }

  const { body: { refreshToken, accessToken }} = response;
  return { refreshToken, accessToken };
}

/**
 *  Fetch a spotify accessToken given a spotify refreshToken.
 */
export async function fetchAccessToken (refreshToken) {

  const response = await request.post(BASE + '/accesstoken')
        .set('Authorization', 'Bearer ' + refreshToken);

  if (response.status !== 200) {
    throw response.body;
  }

  return response.body.accessToken;
}

/**
 *  Souffle a playlist.
 */
export async function souffle (accessToken, playlistUri, souffleBy) {
  const response = await request.post(BASE + '/souffle')
        .set('Authorization', 'Bearer ' + accessToken)
        .send({ playlistUri })
        .send({ souffleBy });

  if (response.status !== 201) {
    throw response.body;
  }

  return response.headers['location'];
}

// -----------
// Spotify API
// -----------

const CLIENT_ID = 'b231329aba1a4c539375436a267db917';
const SPOTIFY_URL = 'https://api.spotify.com/v1';

/**
 *  Redirect the browser to the spotify authorize page.
 */
export const redirectToAuthorizationPage = () => {
  window.location = 'https://accounts.spotify.com/authorize?client_id=' + CLIENT_ID
    + '&response_type=code&redirect_uri=' + REDIRECT_URI
    + '&scope=playlist-read-private%20playlist-modify-private%20playlist-modify-public';
};

/**
 *  Fetch the current user's playlists. Default limit is set to 50.
 */
export async function fetchPlaylists (accessToken, limit = 50) {
  const response = await request.get(SPOTIFY_URL + '/me/playlists')
        .set('Authorization', 'Bearer ' + accessToken)
        .query({ limit });

  return response.body.items.map(
    ({ id, name, uri }) => ({ id, name, uri })
  );
}

/**
 *  Given a spotify playlist uri (i.e. 'spotify:user:zach:playlist:123'), return a path for the
 *  playlist (i.e. '/users/zach/playlists/123').
 */
export const playlistPathFromUri = playlistUri => {
  const substrings = playlistUri.split(':');
  const user = substrings[2];
  const playlist = substrings[4];
  return '/users/' + user + '/playlists/' + playlist;
};

/**
 *  Fetch a playlist object.
 */
export async function fetchPlaylist (accessToken, playlistUri) {
  const playlistPath = playlistPathFromUri(playlistUri);
  const response = await request.get(SPOTIFY_URL + playlistPath)
        .set('Authorization', 'Bearer ' + accessToken)
        .query({ fields: 'name,id,uri' });

  return response.body;

}

/**
 *  Delete (unfollow) a playlist followed by the current user.
 */
export async function deletePlaylist (accessToken, { uri }) {
  const playlistPath = playlistPathFromUri(uri);
  const response = await request.delete(SPOTIFY_URL + playlistPath + '/followers')
        .set('Authorization', 'Bearer ' + accessToken);

  return response;
}
