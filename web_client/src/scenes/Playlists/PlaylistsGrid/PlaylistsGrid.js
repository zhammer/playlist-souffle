import React from 'react';
import styled, { css } from 'react-emotion';
import withIsolationHoverStyles from 'components/withIsolationHoverStyles';
import { TileGrid } from 'components/TileGrid';
import PlaylistTile from './components/PlaylistTile';

const PlaylistsTileGrid = styled(TileGrid)`
  width: 60%;
  min-width: 20em;
  margin: 0 auto;
  margin-bottom: 1em;
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


const Playlists = ({ playlists, onPlaylistSelected }) => (
  <PlaylistsTileGridWithHoverIsolation>
    {playlists.map((playlist, index) => (
      <PlaylistTile
        key={index}
        name={playlist.name}
        onClick={() => onPlaylistSelected(playlist)}
        />
    ))}
  </PlaylistsTileGridWithHoverIsolation>
);

export default Playlists;
