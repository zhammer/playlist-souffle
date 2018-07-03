import { combineReducers } from 'redux';
import auth from './auth';
import playlists from 'scenes/Playlists/PlaylistSelector/reducers';

export default combineReducers({
  auth,
  playlists
});
