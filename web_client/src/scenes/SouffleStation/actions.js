import { push } from 'connected-react-router';
import { playlistSelected } from 'actions/ui';
import { getPlaylists }  from 'selectors';
import { getPathPlaylistId } from './selectors';


export const handleSouffleStationLoaded = () => (dispatch, getState) => {
  const state = getState();
  const pathPlaylistId = getPathPlaylistId(state);
  const playlists = getPlaylists(state);

  const currentPlaylist = playlists.find(playlist => playlist.id === pathPlaylistId);
  if (!currentPlaylist) {
    console.log('hey');
    dispatch(push('/'));
    return;
  }

  dispatch(playlistSelected(currentPlaylist));
};
