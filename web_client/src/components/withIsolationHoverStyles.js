import styled, { css } from 'react-emotion';

const withIsolationHoverStyles = (
  ParentComponent,
  ChildComponent,
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
  `;

  const StyledChildComponent = styled(ChildComponent)`
    &:hover {
      ${childHoveredStyle}
    }
  `;

  return { StyledParentComponent, StyledChildComponent };
};


export default withIsolationHoverStyles;
