import { createSelector } from 'reselect';
import { getPathname } from 'selectors';

const lastSubstring = (string, delim) => {
  const substrings = string.split(delim);
  return substrings[substrings.length - 1];
};

export const getPathPlaylistId = createSelector(
  [getPathname],
  pathname => lastSubstring(pathname, '/')
);
