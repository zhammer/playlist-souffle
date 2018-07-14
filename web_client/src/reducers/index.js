import { combineReducers } from 'redux';
import auth from './auth';
import playlists from './playlists';
import ui from './ui';

export default combineReducers({
  auth,
  playlists,
  ui
});
