import queryString from 'query-string';
import { createSelector } from 'reselect';

export const getPathname = state => state.router.location.pathname;
export const getSearch = state => state.router.location.search;

export const getAuthCode = createSelector(
  [getSearch],
  search => queryString.parse(search).code
);

const lastSubstring = (string, delim) => {
  const substrings = string.split(delim);
  return substrings[substrings.length - 1];
};

export const getPathPlaylistId = createSelector(
  [getPathname],
  pathname => lastSubstring(pathname, '/')
);

export const getSouffledFromId = createSelector(
  [getSearch],
  search => queryString.parse(search).souffledFrom
);
