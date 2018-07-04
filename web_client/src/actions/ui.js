import { push } from 'connected-react-router';

export const SOUFFLE_STARTED = 'SOUFFLE_STARTED';
export const SOUFFLE_SUCCEEDED = 'SOUFFLE_SUCCEEDED';
export const SOUFFLE_BY_UPDATED = 'SOUFFLE_BY_UPDATED';

export const souffleStarted = () => ({
  type: SOUFFLE_STARTED
});

export const souffleSucceeded = () => ({
  type: SOUFFLE_SUCCEEDED
});

export const handlePlaylistSelected = playlist => dispatch => {
  dispatch(push('/playlists/' + playlist.id));
};

export const souffleByUpdated = souffleBy => ({
  type: SOUFFLE_BY_UPDATED,
  payload: { souffleBy }
});

export const handleSouffleByUpdated = souffleBy => dispatch => {
  dispatch(souffleByUpdated(souffleBy));
};
