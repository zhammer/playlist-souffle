import { push } from 'connected-react-router';
import { fetchPlaylistTracks } from 'services/api';
import { souffleStationLoaded } from 'actions/ui';
import { fetchPlaylistTracksStarted, fetchPlaylistTracksSucceeded } from 'actions/playlists';
import { getCurrentPlaylist, getCurrentPlaylistTracks, getAccessToken } from 'selectors';


export const handleSouffleStationLoaded = () => (dispatch, getState) => {
  const state = getState();

  const currentPlaylist = getCurrentPlaylist(state);
  if (!currentPlaylist) {
    // 404
    return;
  }

  if (getCurrentPlaylistTracks(state).length > 0) {
    // tracks already loaded
    return;
  }

  const accessToken = getAccessToken(state);
  dispatch(fetchPlaylistTracksStarted());
  fetchPlaylistTracks(accessToken, currentPlaylist)
    .then(tracks => dispatch(fetchPlaylistTracksSucceeded(currentPlaylist.id, tracks)))
    .catch(err => alert(err));
};
