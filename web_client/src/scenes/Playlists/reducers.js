import { FETCH_PLAYLISTS_SUCCEEDED } from './actions';

const initialState = {
  playlists: {}
};

const playlists = (state = initialState, action) => {
  switch(action.type) {
    case FETCH_PLAYLISTS_SUCCEEDED: {
      return action.payload.playlists;
    }

    default:
      return state;
  }
};

export default playlists;
