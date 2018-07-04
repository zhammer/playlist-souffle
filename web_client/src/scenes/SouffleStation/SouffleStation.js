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
  margin: 0 auto;
  height: 90vh;
`;

// TODO: I should make an h2 or this.
const PlaylistName = styled(StyledH3)`
  display: block;
  text-transform: uppercase;
  margin: 0;
  padding-top: .5em;
  grid-area: title;
  width: 100%;
  transform: scale(1.25);
  overflow: hidden;
  @media (min-width: 35em) {
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

const ARTIST_EMOJI = '\uD83D\uDC69\uD83C\uDFFD\u200D\uD83C\uDFA8';
const ALBUM_EMOJI = '\uD83D\uDCBD';

const SouffleStation = ({ playlist, onSouffleButtonClicked, souffledFrom }) => (
  <Layout>
    <PlaylistName>
      {playlist ? playlist.name : 'Not found'}
    </PlaylistName>
    <Playlist uri={playlist && playlist.uri} />
    {playlist && <SouffleButton onClick={onSouffleButtonClicked}>
        {souffledFrom ? 'ReSouffle' : 'Souffle'} by {ARTIST_EMOJI}
    </SouffleButton>}
  </Layout>
);

export default SouffleStation;
