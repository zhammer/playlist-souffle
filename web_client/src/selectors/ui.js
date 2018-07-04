import { createSelector } from 'reselect';

export const getPathname = state => state.router.location.pathname;
export const getSearch = state => state.router.location.search;

const lastSubstring = (string, delim) => {
  const substrings = string.split(delim);
  return substrings[substrings.length - 1];
};

export const getPathPlaylistId = createSelector(
  [getPathname],
  pathname => lastSubstring(pathname, '/')
);
