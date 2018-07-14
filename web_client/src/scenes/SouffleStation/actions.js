import { push } from 'connected-react-router';
import { fetchPlaylistStarted, fetchPlaylistSucceeded, handlePlaylistDeleted } from 'actions/playlists';
import { souffleStarted, souffleSucceeded, souffleByUpdated } from 'actions/ui';
import { getCurrentPlaylist, getAccessToken, getSouffledFrom, getSouffleBy } from 'selectors';
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


/**
 *  Handle a user toggling the souffleBy button.
 *
 *  Note: It'd probably make sense to just dispatch a souffleByToggled() event and let the reducer
 *  determine the nextSouffleBy. I believe I did it this way as I had initially wanted to use a
 *  souffleBy dropdown so the associated action would be souffleByUpdated with the selected value.
 */
export const handleToggleButtonClicked = () => (dispatch, getState) => {
  const currentSouffleBy = getSouffleBy(getState());
  const nextSouffleBy = currentSouffleBy === 'artist' ? 'album' : 'artist';
  dispatch(souffleByUpdated(nextSouffleBy));
};
