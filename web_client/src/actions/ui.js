import { push } from 'connected-react-router';

export const handlePlaylistSelected = playlist => dispatch => {
  dispatch(push('/playlists/' + playlist.id));
};
