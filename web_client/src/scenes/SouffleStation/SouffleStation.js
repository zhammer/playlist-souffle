import React from 'react';
import styled from 'react-emotion';
import { StyledH3 } from 'components/headers';
import { CtaButton } from 'components/buttons';
import colors from 'theme';
import PlaylistWidget from './components/PlaylistWidget';
// import { TileColumn, Tile } from 'components/TileGrid';

const Layout = styled('div')`
  min-width: 20em;
  max-width: 50em;
  justify-content: center;
  align-items: center;
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 10% 1fr 10%;
  grid-template-areas: ". title ." ". playlist ." "button button button";
  grid-row-gap: 1em;
  width: 100%;
  margin: .5em auto;
  height: 90vh;

  @media (min-width: 35em) {
    margin-top: 1.5em;
  }
`;

const SouffleButton = styled(CtaButton)`
  justify-self: center;
  margin: 0;
  grid-area: button;
  transition: background .5s linear;
  text-shadow: 1px 1px ${colors.darkBlue};
  padding-left: 1.25em;
  padding-right: 1.25em;
  font-size: 1.25rem;

  &:hover {
    background: ${colors.lightYellow};
  }

  @media (min-width: 50em) {
    padding-left: 3em;
    padding-right: 3em;
    font-size: 1.75rem;
  }
`;

const Playlist = styled(PlaylistWidget)`
  width: 100%;
  height: 100%;
  grid-area: playlist;
`;

const Header = styled('div')`
  grid-area: title;
  display: grid;
  grid-template-columns: 10% 1fr 10%;
  margin: 0;
`;

// TODO: I should make an h2 or this.
const PlaylistName = styled(StyledH3)`
  text-transform: uppercase;
  margin: 0;
  align-self: center;
  font-size: 1.5em;
  @media (min-width: 35em) {
    font-size: 2em;
  }
`;

const BackButton = styled('div')`
  text-align: center;
  cursor: pointer;
  align-self: center;
  justify-self: center;
  color ${colors.lightGreen};
  font-size: 1.5rem;
  position:relative;
  width: 100%;

  @media (min-width: 35em) {
    font-size: 2.5rem;
  }

  ::after {
    transition: background .5s linear;
    cursor: pointer;
    position: absolute;
    width: 1em;
    height: 1em;
    content: "";
    z-index: -1;
    border: .1em solid ${colors.lightGreen};
    border-radius: 5em;
    background: ${colors.opaqueWhite};
    left: -.325em;
    top: .125em;

    left: 0;
    right: 0;
    margin: 0 auto;
  }

  &:hover::after {
    background: ${colors.opaqueLightGreen};
  }
`;

const ARTIST_EMOJI = '\uD83D\uDC69\uD83C\uDFFD\u200D\uD83C\uDFA8';
const ALBUM_EMOJI = '\uD83D\uDCBD';

const SouffleStation = ({ playlist, onSouffleButtonClicked, souffledFrom, souffleBy, onBackButtonClicked }) => (
  <Layout>
    <Header>
      <BackButton onClick={onBackButtonClicked}>{'<'}</BackButton>
      <PlaylistName>
        {playlist ? playlist.name : 'Not found'}
      </PlaylistName>
    </Header>
    <Playlist uri={playlist && playlist.uri} />
    {playlist && <SouffleButton onClick={onSouffleButtonClicked}>
        {souffledFrom ? 'ReSouffle' : 'Souffle'} by {souffleBy === 'artist' ? ARTIST_EMOJI : ALBUM_EMOJI }
    </SouffleButton>}
  </Layout>
);

export default SouffleStation;
