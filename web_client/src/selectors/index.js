import { createSelector } from 'reselect';
import { getAccessToken, getFetchingAccessToken, getFetchingRefreshToken } from './auth';
import { getPlaylists, getFetchingPlaylists } from './playlists';
import { getPathPlaylistId } from './ui';

export { getAccessToken, getFetchingAccessToken, getPlaylists, getFetchingPlaylists, getPathPlaylistId };

export const getLoading = createSelector(
  [getFetchingAccessToken, getFetchingPlaylists, getFetchingRefreshToken],
  (fetchingAccessToken, fetchingPlaylists, fetchingRefreshToken) =>
    fetchingAccessToken || fetchingPlaylists || fetchingRefreshToken
);

export const getCurrentPlaylist = createSelector(
  [getPlaylists, getPathPlaylistId],
  (playlists, pathPlaylistId) =>
    pathPlaylistId && playlists.find(playlist => playlist.id === pathPlaylistId)
);

export const getCurrentPlaylistTracks = createSelector(
  [getCurrentPlaylist],
  currentPlaylist => (currentPlaylist && currentPlaylist.tracks) || []
);
