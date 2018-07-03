import React from 'react';
import { StyledH3 } from 'components/headers';

const SouffleStation = ({ playlist }) => (
  <StyledH3>
    My playlist: {JSON.stringify(playlist)}
  </StyledH3>
);

export default SouffleStation;
