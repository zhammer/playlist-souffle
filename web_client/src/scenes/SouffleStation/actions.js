import { push } from 'connected-react-router';
import { fetchPlaylistStarted, fetchPlaylistSucceeded, handlePlaylistDeleted } from 'actions/playlists';
import { souffleStarted, souffleSucceeded } from 'actions/ui';
import { getCurrentPlaylist, getAccessToken, getSouffledFrom } from 'selectors';
import { souffle, fetchPlaylist } from 'services/api';

export const handleSouffleButtonClicked = () => (dispatch, getState) => {
  const state = getState();
  const currentPlaylist = getCurrentPlaylist(state);
  const accessToken = getAccessToken(state);
  const souffledFrom = getSouffledFrom(state);
  const originalPlaylist = souffledFrom || currentPlaylist;

  dispatch(souffleStarted());
  souffle(accessToken, originalPlaylist.uri, 'album')
    .then(souffledUri => {
      dispatch(fetchPlaylistStarted());
      fetchPlaylist(accessToken, souffledUri)
        .then(playlist => {
          dispatch(fetchPlaylistSucceeded(playlist));
          dispatch(souffleSucceeded());
          dispatch(push('/playlists/' + playlist.id + '?souffledFrom=' + originalPlaylist.id));
          if (souffledFrom) {
            dispatch(handlePlaylistDeleted(currentPlaylist));
          }
        });
    })
    .catch(err => alert(err));
};


export const handleBackButtonClicked = () => dispatch => {
  dispatch(push('/playlists'));
};
