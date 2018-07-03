import React from 'react';
import styled, { css } from 'react-emotion';
import { StyledH4 } from 'components/headers';
import colors from 'theme';

const Container = styled('div')`
  background-color: ${colors.opaqueWhite};
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: .1em;
  margin: .25em;
  height: 3em;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.15rem;
  cursor: pointer;

  @media (min-width: 35em) {
    height: 3.5em;
    margin: .5em;
  }
`;

const Playlist = ({ name, className }) => (
  <Container className={className}>
    <StyledH4 className={css`margin: .5em;`}>{name}</StyledH4>
  </Container>
);

export default Playlist;
