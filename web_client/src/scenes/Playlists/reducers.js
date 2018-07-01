import { FETCH_PLAYLISTS_SUCCEEDED } from './actions';

const playlists = (state = {}, action) => {
  switch(action.type) {
    case FETCH_PLAYLISTS_SUCCEEDED: {
      return action.payload.playlists;
    }

    default:
      return state;
  }
};
