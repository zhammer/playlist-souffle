import { FETCH_PLAYLISTS_STARTED, FETCH_PLAYLISTS_SUCCEEDED } from 'actions/playlists';

const initialState = {
  playlists: {},
  fetchingPlaylists: false
};

const playlists = (state = initialState, action) => {
  switch(action.type) {
    case FETCH_PLAYLISTS_SUCCEEDED: {
      return {
        playlists: action.payload.playlists,
        fetchPlaylists: false
      };
    }

    case FETCH_PLAYLISTS_STARTED:
      return {
        ...state,
        fetchingPlaylists: true
      };

    default:
      return state;
  }
};

export default playlists;
