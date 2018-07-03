import { createSelector } from 'reselect';
import { getAccessToken, getFetchingAccessToken, getFetchingRefreshToken } from './auth';
import { getPlaylists, getFetchingPlaylists } from './playlists';
import { getCurrentPlaylist } from './ui';

export { getAccessToken, getFetchingAccessToken, getPlaylists, getFetchingPlaylists, getCurrentPlaylist };

export const getLoading = createSelector(
  [getFetchingAccessToken, getFetchingPlaylists, getFetchingRefreshToken],
  (fetchingAccessToken, fetchingPlaylists, fetchingRefreshToken) =>
    fetchingAccessToken || fetchingPlaylists || fetchingRefreshToken
);

// Selectors for connected-react-router

export const getPathname = state => state.router.location.pathname;
export const getSearch = state => state.router.location.search;
