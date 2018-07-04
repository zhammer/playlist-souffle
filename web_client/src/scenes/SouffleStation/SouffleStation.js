import React from 'react';
import styled from 'react-emotion';
import { StyledH3 } from 'components/headers';
import { CtaButton } from 'components/buttons';
import colors from 'theme';
import PlaylistWidget from './components/PlaylistWidget';
// import { TileColumn, Tile } from 'components/TileGrid';

const Layout = styled('div')`
  width: 60%;
  min-width: 25em;
  max-width: 50em;
  margin: 0 auto;
  display: grid;
  max-height: 100vh;
  grid-template-columns: 1fr;
  grid-template-rows: auto auto auto;
  grid-template-areas: "title"
                       "tracks"
                       "button";
`;

// TODO: I should make an h2 or this.
const PlaylistName = styled(StyledH3)`
  text-transform: uppercase;
  margin: 1em;
  transform: scale(1.25);
  grid-area: title;
`;

const SouffleButton = styled(CtaButton)`
  grid-area: button;
  justify-self: center;
  margin: 1em;
  transition: background .5s linear;
  text-shadow: 1px 1px ${colors.darkBlue};

  &:hover {
    background: ${colors.lightYellow};
  }
`;

const Playlist = styled(PlaylistWidget)`
  grid-area: tracks;
  width: 100%;
  height: 35em;
  border-radius: 5em !important;
`;

const SouffleStation = ({ playlist }) => (
  <Layout>
    <PlaylistName>
      {playlist && playlist.name}
    </PlaylistName>
    <Playlist uri={playlist && playlist.uri} />
    <SouffleButton>Souffle</SouffleButton>
  </Layout>
);

export default SouffleStation;
