import {
  FETCH_PLAYLISTS_STARTED,
  FETCH_PLAYLISTS_SUCCEEDED,
  FETCH_PLAYLIST_TRACKS_STARTED,
  FETCH_PLAYLIST_TRACKS_SUCCEEDED
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
        fetchPlaylists: false
      };
    }

    case FETCH_PLAYLISTS_STARTED:
      return {
        ...state,
        fetchingPlaylists: true
      };

    case FETCH_PLAYLIST_TRACKS_STARTED:
      return {
        ...state,
        fetchingTracks: true
      };

    case FETCH_PLAYLIST_TRACKS_SUCCEEDED: {
      const { payload: { playlistId, tracks } } = action;
      const nextPlaylists = state.playlists.map(
        playlist => playlist.id === playlistId ? { ...playlist, tracks } : playlist
      );
      return {
        ...state,
        playlists: nextPlaylists,
        fetchingTracks: false
      };
    }

    default:
      return state;
  }
};

export default playlists;
