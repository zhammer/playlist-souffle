import React from 'react';

import styled, { keyframes } from 'react-emotion';

import colors, { artistEmoji, albumEmoji } from 'theme';
import { StyledH1, StyledH3, StyledH4 } from 'components/headers';
import { SpotifyButton } from 'components/buttons';

import SouffleHero from './components/SouffleHero';

const UnderlinedH3 = styled(StyledH3)`

`;

const YellowOnHover = styled('span')`
  &:hover {
    color: ${colors.yellow};
  }
`;

const fadein = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const Title = styled(StyledH3)`
  text-decoration: underline;
  animation: ${fadein} .5s ease-in both;
`;

const Subtitle = styled(StyledH4)`
  animation: ${fadein} 1s ease-in 1.5s both;
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
    <Title><YellowOnHover>Souffle</YellowOnHover> up your playlists</Title>
    <Subtitle>
      Swap out each track with another track on the same album {albumEmoji} or by the same artist {artistEmoji}.
    </Subtitle>
    <SouffleHero />
    <ButtonContainer>
      <SpotifyButton onClick={onLoginButtonClicked}>Login</SpotifyButton>
    </ButtonContainer>
  </div>
);

export default Landing;
