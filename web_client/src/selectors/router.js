import queryString from 'query-string';
import { createSelector } from 'reselect';

export const getPathname = state => state.router.location.pathname;
export const getSearch = state => state.router.location.search;

/**
 *  Get the auth code from the current routes query params (i.e. '...?code={authcode}') if it exists,
 *  otherwise return null.
 */
export const getAuthCode = createSelector(
  [getSearch],
  search => queryString.parse(search).code
);

/**
 *  Given a string and a delimiter, split the string into substrings and return the last substring.
 *  ex: lastSubstring('hey-there-joe', '-') => 'joe'
 */
const lastSubstring = (string, delim) => {
  const substrings = string.split(delim);
  return substrings[substrings.length - 1];
};

/**
 *  Get the playlist id from the current route (i.e. '.../playlists/{id}').
 *  Note: If needed this could explicitly return null if the route is not at 'playlists/{id}'.
 */
export const getPathPlaylistId = createSelector(
  [getPathname],
  pathname => lastSubstring(pathname, '/')
);

/**
 *  Get the '?souffleFrom={playlistId}' from the current route.
 */
export const getSouffledFromId = createSelector(
  [getSearch],
  search => queryString.parse(search).souffledFrom
);
