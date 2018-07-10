import { createSelector } from 'reselect';
import { getAccessToken, getFetchingAccessToken, getFetchingRefreshToken } from './auth';
import { getPlaylists, getFetchingPlaylists } from './playlists';
import { getSouffleing, getSouffleBy } from './ui';
import { getAuthCode, getSouffledFromId, getPathPlaylistId, } from './router';

export { getAccessToken, getFetchingAccessToken, getPlaylists, getFetchingPlaylists, getPathPlaylistId, getSouffleBy, getAuthCode };

/**
 *  Get whether or not the application is in a state of loading some data.
 */
export const getLoading = createSelector(
  [getFetchingAccessToken, getFetchingPlaylists, getFetchingRefreshToken, getSouffleing],
  (fetchingAccessToken, fetchingPlaylists, fetchingRefreshToken, souffleing) =>
    fetchingAccessToken || fetchingPlaylists || fetchingRefreshToken || souffleing
);

/**
 *  Get the current playlist if there is one, otherwise return null.
 */
export const getCurrentPlaylist = createSelector(
  [getPlaylists, getPathPlaylistId],
  (playlists, pathPlaylistId) =>
    pathPlaylistId && playlists.find(playlist => playlist.id === pathPlaylistId)
);

/**
 *  Get the playlist the current playlist was souffled from if there is one, otherwise return null.
 */
export const getSouffledFrom = createSelector(
  [getPlaylists, getSouffledFromId],
  (playlists, souffledFromId) =>
    souffledFromId && playlists.find(playlist => playlist.id === souffledFromId)
);
