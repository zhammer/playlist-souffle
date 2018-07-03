import styled, { css } from 'react-emotion';

const withIsolationHoverStyles = (
  ParentComponent,
  childHoveredStyle,
  childIgnoredStyle,
  transitionStyle=css`transition: all .5s ease-out;`
) => {
  const StyledParentComponent = styled(ParentComponent)`
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
  `;

  return StyledParentComponent;
};


export default withIsolationHoverStyles;
