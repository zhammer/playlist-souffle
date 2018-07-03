import React from 'react';
import styled, { css } from 'react-emotion';
import withIsolationHoverStyles from 'components/withIsolationHoverStyles';
import { TileGrid } from 'components/TileGrid';
import Playlist from './components/Playlist';

const PlaylistsTileGrid = styled(TileGrid)`
  width: 60%;
  min-width: 20em;
  margin: 0 auto;
`;

const hoveredStyle = css`
  transform: scale(1.05);
  opacity: 1;
`;

const ignoredStyle = css`
  opacity: .5;
`;

const transitionStyle = css`
  transition: all .5s ease-out;
`;

const PlaylistsTileGridWithHoverIsolation = withIsolationHoverStyles(
  PlaylistsTileGrid,
  hoveredStyle,
  ignoredStyle,
  transitionStyle
);


const Playlists = ({ playlists }) => (
  <PlaylistsTileGridWithHoverIsolation>
    {playlists.map((playlist, index) => (
      <Playlist key={index} name={playlist.name} />
    ))}
  </PlaylistsTileGridWithHoverIsolation>
);

export default Playlists;
