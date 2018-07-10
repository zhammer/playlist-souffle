import React from 'react';
import styled from 'react-emotion';
import Morpher from './components/Morpher';

const Container = styled('div')`
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Loading = () => (
  <Container>
    <Morpher />
  </Container>
);

export default Loading;
