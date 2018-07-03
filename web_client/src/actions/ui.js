import { push } from 'connected-react-router';

export const PLAYLIST_SELECTED = 'PLAYLIST_SELECTED';

// right now this is updated by the souffle station page on load (to handle for fresh loading
// on /playlists/my_playlist_id
export const playlistSelected = playlist => ({
  type: PLAYLIST_SELECTED,
  payload: {
    playlist
  }
});

export const handlePlaylistSelected = playlist => dispatch => {
  dispatch(push('/playlists/' + playlist.id));
};
