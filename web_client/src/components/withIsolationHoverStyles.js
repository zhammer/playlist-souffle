import styled, { css } from 'react-emotion';

/**
 *  Style a parent component so that upon hovering over one of its children, that child is isolated
 *  from the non-hovered children.
 *
 *  When hovering over a ComponentWithIsolationHoverStyles' children, the hovered child will
 *  display a `childHoveredStyle` and all other elements will display a `childIgnoredStyle`,
 *  with a transition specified by `transitionStyle`.
 *
 *  Styling a parent component with this function disables pointer-events on the parent component.
 *
 *  Inspired by Sarah Drasner's example from SVG Animations: https://codepen.io/sdras/details/qOdWEP.
 */
const withIsolationHoverStyles = (
  ParentComponent,
  childHoveredStyle,
  childIgnoredStyle,
  transitionStyle=css`transition: all .5s ease-out;`
) => (
  styled(ParentComponent)`
    pointer-events: none;
    & > * {
      pointer-events: auto;
      ${transitionStyle}
    }

    &:hover > * {
      ${childIgnoredStyle}
    }

    &:hover > *:hover {
      ${childHoveredStyle}
    }
  `
);


export default withIsolationHoverStyles;
