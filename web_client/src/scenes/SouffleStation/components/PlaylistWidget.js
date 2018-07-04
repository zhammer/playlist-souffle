import React from 'react';

const PlaylistWidget = ({ uri, className }) => (
  <iframe
    className={className}
    src={'https://open.spotify.com/embed?uri=' + uri}
    frameborder="0"
    allowtransparency="true"
    allow="encrypted-media">
  </iframe>
);

export default PlaylistWidget;
