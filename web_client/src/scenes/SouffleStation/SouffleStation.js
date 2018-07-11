import React from 'react';
import styled from 'react-emotion';
import { StyledH3 } from 'components/headers';
import colors from 'theme';
import SouffleButton from './components/SouffleButton';
import PlaylistWidget from './components/PlaylistWidget';

const Layout = styled('div')`
  width: 100%;
  min-width: 20em;
  max-width: 50em;
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 10% 1fr 10%;
  grid-template-areas: "back  title    ."
                       ".     playlist ."
                       ".     button   .";
  grid-row-gap: 1em;
  justify-content: center;
  align-items: center;
  margin: .5em auto;
  padding-left: .5em;
  padding-right: .5em;
  height: 90vh;

  @media (min-width: 35em) {
    margin-top: 1.5em;
  }
`;

const Playlist = styled(PlaylistWidget)`
  width: 100%;
  height: 100%;
  grid-area: playlist;
`;

const PlaylistName = styled(StyledH3)`
  text-transform: uppercase;
  margin: 0;
  grid-area: title;
  align-self: center;
  font-size: 1.5em;
  @media (min-width: 35em) {
    font-size: 2em;
  }
`;

// Note: I should make this as an svg img rather than the pseudo stuff (which is from CSS in Depth).
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

const SouffleButtonContainer = styled('div')`
  grid-area: button;
  justify-self: center;
  width: 100%;
`;

const BACK_ARROW = '<'; // saving as var is just to fix an annoying editor spacing indentation glitch

const SouffleStation = ({ playlist, onSouffleButtonClicked, onToggleButtonClicked, souffledFrom, souffleBy, onBackButtonClicked }) => (
  <Layout>
    <BackButton onClick={onBackButtonClicked}>{BACK_ARROW}</BackButton>
    <PlaylistName>
      {playlist ? playlist.name : 'Not found'}
    </PlaylistName>
    <Playlist uri={playlist && playlist.uri} />
    <SouffleButtonContainer>
      {playlist && <SouffleButton
                       souffleBy={souffleBy}
                       isResouffle={!!souffledFrom}
                       onSouffleButtonClicked={onSouffleButtonClicked}
                       onToggleButtonClicked={onToggleButtonClicked}/>
      }
    </SouffleButtonContainer>
</Layout>
);

export default SouffleStation;
