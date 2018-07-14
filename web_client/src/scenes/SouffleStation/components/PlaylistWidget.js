import React from 'react';
import styled from 'react-emotion';

const Frame = styled('div')`
  border-radius: 1em;
  overflow: hidden;
`;

/**
 *  A wrapper component for a Spotify Play Button iframe. Adds a rounded border to the rectangular
 *  iframe view.
 */
const PlaylistWidget = ({ uri, className }) => (
  <Frame className={className}>
    <iframe
      title={uri}
      src={'https://open.spotify.com/embed?uri=' + uri}
      frameBorder="0"
      allowtransparency="true"
      width='100%'
      height='100%'
      allow="encrypted-media">
    </iframe>
  </Frame>
);

export default PlaylistWidget;
