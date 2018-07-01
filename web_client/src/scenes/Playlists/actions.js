import { fetchPlaylists } from 'services/api';
import { getAccessToken } from 'selectors';

const FETCH_PLAYLISTS_SUCCEEDED = 'FETCH_PLAYLISTS_SUCCEEDED';

const fetchPlaylistsSucceeded = (playlists) => ({
  type: FETCH_PLAYLISTS_SUCCEEDED,
  payload: {
    playlists
  }
});

const handlePlaylistsPageLoaded = () => (dispatch, getState) => {
  const state = getState();
  const accessToken = getAccessToken(state);

  fetchPlaylists(accessToken)
    .then(playlists => fetchPlaylistsSucceeded(playlists))
    .catch(err => console.log(err)); // Should clear accesstoken
};
