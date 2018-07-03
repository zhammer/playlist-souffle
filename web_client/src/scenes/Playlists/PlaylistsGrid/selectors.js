import { createSelector } from 'reselect';
import { getFetchingAccessToken } from 'selectors';

export const getPlaylists = state => Object.values(state.playlists.playlists);
export const getFetchingPlaylists = state => state.playlists.fetchingPlaylists;

export const getPlaylistsPageLoading = createSelector(
  [getFetchingAccessToken, getFetchingPlaylists],
  (fetchingAccessToken, fetchingPlaylists) => fetchingAccessToken || fetchingPlaylists
);
