import React from 'react';

import styled from 'react-emotion';

import colors, { artistEmoji, albumEmoji } from 'theme';
import { StyledH1, StyledH3, StyledH4 } from 'components/headers';
import { SpotifyButton } from 'components/buttons';

import SouffleHero from './components/SouffleHero';

const UnderlinedH3 = styled(StyledH3)`
  text-decoration: underline;
`;

const YellowOnHover = styled('span')`
  &:hover {
    color: ${colors.yellow};
  }
`;

const ButtonContainer = styled('div')`
  margin-top: 1.75em;
  margin-bottom: 2em;
  display: flex;
  justify-content: center;

  @media (min-width: 35em) {
    margin-top: 3em;
  }
`;

const Landing = ({ onLoginButtonClicked }) => (
  <div className="Landing">
    <StyledH1>Playlist Souffle</StyledH1>
    <UnderlinedH3><YellowOnHover>Souffle</YellowOnHover> up your playlists</UnderlinedH3>
    <StyledH4>
      Swap out each track with another track on the same album {albumEmoji} or by the same artist {artistEmoji}.
    </StyledH4>
    <SouffleHero />
    <ButtonContainer>
      <SpotifyButton onClick={onLoginButtonClicked}>Login</SpotifyButton>
    </ButtonContainer>
  </div>
);

export default Landing;
