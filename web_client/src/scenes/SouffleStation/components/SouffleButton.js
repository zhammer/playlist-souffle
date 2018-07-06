import React from 'react';
import styled from 'react-emotion';
import ReactCSSTransitionReplace from 'react-css-transition-replace';
import colors, { artistEmoji, albumEmoji } from 'theme';
import { CtaButton } from 'components/buttons';
import BackForthIcon from './BackForthSvg';
import './crossfade.css';

const emojiBySouffleType = {
  artist: artistEmoji,
  album: albumEmoji
};

// TODO: This is a pain in the a** but whatever. I want the emoji to fade.
const souffleButtonText = (isResouffle, souffleBy) => {
  const emoji = emojiBySouffleType[souffleBy];
  const text = (isResouffle ? 'ReSouffle' : 'Souffle') + ' by ' + emoji;
  return (
      <ReactCSSTransitionReplace
        transitionName='cross-fade'
        transitionEnterTimeout={500}
        transitionLeaveTimeout={500}>
        <div key={text}>{text}</div>
      </ReactCSSTransitionReplace>
  );
};

const Layout = styled('div')`
  display: grid;
  grid-template-columns: 80% 1fr;
  grid-column-gap: .25em;
  margin: 0;


  @media (min-width: 35em) {
    font-size: 1.75rem;
    margin: 0 3em;
  }

  @media (min-width: 50em) {
    font-size: 1.75rem;
    margin: 0 3em;
  }

`;

const Base = styled(CtaButton)`
  padding-left: 0;
  padding-right: 0;
  margin: 0;
  transition: background .5s linear;
  text-shadow: 1px 1px ${colors.darkBlue};
  font-size: 1.25rem;

  &:hover {
    background: ${colors.lightYellow};
  }
`

const StyledButtonLeft = styled(Base)`
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-right-width: .15em;

`;

const StyledButtonRight = styled(Base)`
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  border-left-width: .15em;
  position: relative;
`;

// I need to learn how to actually use svgs..
const StyledIcon = styled(BackForthIcon)`
  fill: ${colors.yellow};
  stroke: ${colors.yellow};

  position: absolute;
  transform: scale(.15);
  left: -3.9em;
  top: -2.3em;


  @media (min-width: 35em) {
    transform: scale(.15);
    top: -2.4em;
    left: -3.75em;
  }

  @media (min-width: 50em) {
    transform: scale(.2);
    top: -1.05em;
    left: -2em;
  }
`;

const SouffleButton = ({ isResouffle, souffleBy, onSouffleButtonClicked, onToggleButtonClicked }) => (
  <Layout>
    <StyledButtonLeft onClick={onSouffleButtonClicked}>{souffleButtonText(isResouffle, souffleBy)}</StyledButtonLeft>
    <StyledButtonRight onClick={onToggleButtonClicked}><StyledIcon/></StyledButtonRight>
  </Layout>
);

export default SouffleButton;
