import { SOUFFLE_STARTED, SOUFFLE_SUCCEEDED } from 'actions/ui';

const initialState = {
  souffleing: false
};

const ui = (state = initialState, action) => {
  switch(action.type) {
    case SOUFFLE_STARTED:
      return { ...state, souffleing: true };

    case SOUFFLE_SUCCEEDED:
      return { ...state, souffleing: false };

    default:
      return state;
  }
};

export default ui;
