import React from 'react';
import styled from 'react-emotion';

const Frame = styled('div')`
  border-radius: 1em;
  overflow:hidden;
`;

const PlaylistWidget = ({ uri, className }) => (
  <Frame className={className}>
    <iframe
      src={'https://open.spotify.com/embed?uri=' + uri}
      frameborder="0"
      allowtransparency="true"
      width='100%'
      height='100%'
      allow="encrypted-media">
    </iframe>
  </Frame>
);

export default PlaylistWidget;
