import React from 'react';
import styled from 'react-emotion';
import { StyledH3 } from 'components/headers';
import { CtaButton } from 'components/buttons';
import colors from 'theme';
import PlaylistWidget from './components/PlaylistWidget';
// import { TileColumn, Tile } from 'components/TileGrid';

const Layout = styled('div')`
  width: 60%;
  min-width: 20em;
  max-width: 50em;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 90vh;

`;

// TODO: I should make an h2 or this.
const PlaylistName = styled(StyledH3)`
  text-transform: uppercase;
  margin: 1em;
  transform: scale(1.25);
  display: none;

  @media (min-width: 35em) {
    display: inherit;
  }
`;

const SouffleButton = styled(CtaButton)`
  justify-self: center;
  margin: 1em;
  margin-top: .5em;
  transition: background .5s linear;
  text-shadow: 1px 1px ${colors.darkBlue};
  padding-left: 2.25em;
  padding-right: 2.25em;

  &:hover {
    background: ${colors.lightYellow};
  }

  @media (min-width: 50em) {
    padding-left: 3em;
    padding-right: 3em;
    margin: 1em;
    font-size: 1.75rem;
  }
`;

const Playlist = styled(PlaylistWidget)`
  margin-top: 1em;
  width: 100%;
  flex: 1 1 70%;
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
