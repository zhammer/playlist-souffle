import React from 'react';
import { css } from 'react-emotion';
import { StyledH4 } from 'components/headers';
import { Tile } from 'components/TileGrid';

const Playlist = ({ name, className }) => (
  <Tile className={className}>
    <StyledH4 className={css`margin: .5em;`}>{name}</StyledH4>
  </Tile>
);

export default Playlist;
