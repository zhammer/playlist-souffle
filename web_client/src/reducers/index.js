import { combineReducers } from 'redux';
import auth from './auth';
import playlists from './playlists';

export default combineReducers({
  auth,
  playlists
});
