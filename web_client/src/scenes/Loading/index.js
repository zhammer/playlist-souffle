import React from 'react';
import styled from 'react-emotion';
import { StyledH3 } from 'components/headers';

const Container = styled('div')`
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Loading = () => (
  <Container>
    <StyledH3>Loading</StyledH3>
  </Container>
);

export default Loading;
