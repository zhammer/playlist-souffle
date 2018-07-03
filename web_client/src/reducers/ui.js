import { PLAYLIST_SELECTED } from 'actions/ui';

const initialState = {
  currentPlaylist: null
};

const ui = (state = initialState, action) => {
  switch(action.type) {
    case PLAYLIST_SELECTED:
      return {
        ...state,
        currentPlaylist: action.payload.playlist
      };

    default:
      return state;
  }
};


export default ui;
