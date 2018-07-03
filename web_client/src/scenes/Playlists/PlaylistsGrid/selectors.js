import { createSelector } from 'reselect';
import { getFetchingAccessToken, getFetchingPlaylists } from 'selectors';

export const getPlaylistsPageLoading = createSelector(
  [getFetchingAccessToken, getFetchingPlaylists],
  (fetchingAccessToken, fetchingPlaylists) => fetchingAccessToken || fetchingPlaylists
);
