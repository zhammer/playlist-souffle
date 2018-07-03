import React from 'react';
import styled, { css } from 'react-emotion';
import withIsolationHoverStyles from 'components/withIsolationHoverStyles';
import { StyledH3 } from 'components/headers';
import Playlist from './components/Playlist';

// TODO: Move the tiling grid (Playlists) and tile (Playlist) components to top-level components.
const Container = styled('div')`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20em, 1fr));
  grid-auto-rows: 1fr;
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

const {
  StyledParentComponent: StyledContainer,
  StyledChildComponent: StyledPlaylist
} = withIsolationHoverStyles(
  Container,
  Playlist,
  hoveredStyle,
  ignoredStyle,
  transitionStyle
);


const Playlists = ({ playlists }) => (
  <StyledContainer>
    {playlists.map((playlist, index) => (
      <StyledPlaylist key={index} name={playlist.name} />
    ))}
  </StyledContainer>
);

export default Playlists;
