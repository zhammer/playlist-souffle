import {
  FETCH_REFRESH_TOKEN_SUCCEEDED,
  FETCH_ACCESS_TOKEN_SUCCEEDED,
  FETCH_REFRESH_TOKEN_STARTED,
  FETCH_ACCESS_TOKEN_STARTED
} from 'actions/auth';

const initialState = {
  accessToken: null,
  refreshToken: null,
  fetchingAccessToken: false,
  fetchingRefreshToken: false
};

const auth = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_REFRESH_TOKEN_SUCCEEDED: {
      const { refreshToken } = action.payload;
      return {
        ...state,
        refreshToken,
        fetchingRefreshToken: false
      };
    }

    case FETCH_ACCESS_TOKEN_SUCCEEDED: {
      const { accessToken } = action.payload;
      return {
        ...state,
        accessToken,
        fetchingAccessToken: false
      };
    }

    case FETCH_REFRESH_TOKEN_STARTED:
      return {
        ...state,
        fetchingRefreshToken: true
      };

    case FETCH_ACCESS_TOKEN_STARTED:
      return {
        ...state,
        fetchingAccessToken: true
      };



    default:
      return state;
  }
};

export default auth;
