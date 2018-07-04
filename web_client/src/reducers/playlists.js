import {
  FETCH_PLAYLISTS_STARTED,
  FETCH_PLAYLISTS_SUCCEEDED,
  FETCH_PLAYLIST_STARTED,
  FETCH_PLAYLIST_SUCCEEDED,
} from 'actions/playlists';

const initialState = {
  playlists: {},
  fetchingPlaylists: false,
  fetchingTracks: false
};

const playlists = (state = initialState, action) => {
  switch(action.type) {
    case FETCH_PLAYLISTS_SUCCEEDED: {
      return {
        playlists: action.payload.playlists,
        fetchingPlaylists: false
      };
    }

    case FETCH_PLAYLISTS_STARTED:
      return {
        ...state,
        fetchingPlaylists: true
      };

    case FETCH_PLAYLIST_SUCCEEDED: {
      const { playlists } = state;
      return {
        playlists: [action.payload.playlist, ...playlists],
        fetchingPlaylists: false
      };
    }

    case FETCH_PLAYLIST_STARTED:
      return {
        ...state,
        fetchingPlaylists: true
      };

    default:
      return state;
  }
};

export default playlists;
