import { createSelector } from 'reselect';
import { getAccessToken, getFetchingAccessToken, getFetchingRefreshToken } from './auth';
import { getPlaylists, getFetchingPlaylists } from './playlists';
import { getSouffleing, getSouffleBy } from './ui';
import { getAuthCode, getSouffledFromId, getPathPlaylistId, } from './router';

export { getAccessToken, getFetchingAccessToken, getPlaylists, getFetchingPlaylists, getPathPlaylistId, getSouffleBy, getAuthCode };

export const getLoading = createSelector(
  [getFetchingAccessToken, getFetchingPlaylists, getFetchingRefreshToken, getSouffleing],
  (fetchingAccessToken, fetchingPlaylists, fetchingRefreshToken, souffleing) =>
    fetchingAccessToken || fetchingPlaylists || fetchingRefreshToken || souffleing
);

export const getCurrentPlaylist = createSelector(
  [getPlaylists, getPathPlaylistId],
  (playlists, pathPlaylistId) =>
    pathPlaylistId && playlists.find(playlist => playlist.id === pathPlaylistId)
);

export const getSouffledFrom = createSelector(
  [getPlaylists, getSouffledFromId],
  (playlists, souffledFromId) =>
    souffledFromId && playlists.find(playlist => playlist.id === souffledFromId)
);
