import { push } from 'connected-react-router';

export const SOUFFLE_STARTED = 'SOUFFLE_STARTED';
export const SOUFFLE_SUCCEEDED = 'SOUFFLE_SUCCEEDED';

export const souffleStarted = () => ({
  type: SOUFFLE_STARTED
});

export const souffleSucceeded = () => ({
  type: SOUFFLE_SUCCEEDED
});

export const handlePlaylistSelected = playlist => dispatch => {
  dispatch(push('/playlists/' + playlist.id));
};
