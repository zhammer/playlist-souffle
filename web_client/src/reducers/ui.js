import { SOUFFLE_STARTED, SOUFFLE_SUCCEEDED, SOUFFLE_BY_UPDATED } from 'actions/ui';

const initialState = {
  souffleing: false,
  souffleBy: 'artist'
};

const ui = (state = initialState, action) => {
  switch(action.type) {
    case SOUFFLE_STARTED:
      return { ...state, souffleing: true };

    case SOUFFLE_SUCCEEDED:
      return { ...state, souffleing: false };

    case SOUFFLE_BY_UPDATED:
      return { ...state, souffleBy: action.payload.souffleBy};

    default:
      return state;
  }
};

export default ui;
