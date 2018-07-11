import React from 'react';
import styled, { css } from 'react-emotion';
import ReactCSSTransitionReplace from 'react-css-transition-replace';
import colors, { artistEmoji, albumEmoji } from 'theme';
import { CtaButton } from 'components/buttons';
import BackForthIcon from './BackForthSvg';

const emojiBySouffleType = {
  artist: artistEmoji,
  album: albumEmoji
};

/**
 *  Crossfade css transition classes for a ReactCSSTransition.
 */
const crossFade = css`
  &-leave {
    opacity: 1;
  }
  &-leave&-leave-active {
    opacity: 0;
    transition: opacity .5s ease-out;
  }
  &-enter {
    opacity: 0;
  }
  &-enter&-enter-active {
    opacity: 1;
    transition: opacity .5s ease-out;
  }
`;

/**
 *  This is a very annoying way to get the artist / album emoji to crossfade when changed.
 */
const souffleButtonText = (isResouffle, souffleBy) => {
  const emoji = emojiBySouffleType[souffleBy];
  const text = (isResouffle ? 'ReSouffle' : 'Souffle') + ' by ' + emoji;
  return (
      <ReactCSSTransitionReplace
        transitionName={crossFade}
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
  display: flex;
  justify-content: center;
  align-items: center;
`;

const StyledIcon = styled(BackForthIcon)`
  fill: ${colors.yellow};
  stroke: ${colors.yellow};
  margin-right: .25em;
  height: 1.25em;
  width: 1.25em;
`;

/**
 *  The SouffleButton is a button with a left sub button (to Souffle the playlist) and a right sub
 *  button (to toggle the current souffleBy mode). The basic left/right component should really be
 *  moved to a SplitButton component.
 */
const SouffleButton = ({ isResouffle, souffleBy, onSouffleButtonClicked, onToggleButtonClicked }) => (
  <Layout>
    <StyledButtonLeft onClick={onSouffleButtonClicked}>{souffleButtonText(isResouffle, souffleBy)}</StyledButtonLeft>
    <StyledButtonRight onClick={onToggleButtonClicked}><StyledIcon/></StyledButtonRight>
  </Layout>
);

export default SouffleButton;
