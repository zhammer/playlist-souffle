import { FETCH_REFRESH_TOKEN_SUCCEEDED } from 'actions/auth';

const auth = (state={}, action) => {
  switch (action.type) {
    case FETCH_REFRESH_TOKEN_SUCCEEDED: {
      const { refreshToken, accessToken } = action.payload;
      return {
        ...state,
        refreshToken,
        accessToken
      };
    }

    default:
      return state;
  }
};

export default auth;
