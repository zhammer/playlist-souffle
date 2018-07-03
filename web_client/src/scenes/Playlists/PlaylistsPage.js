import React from 'react';
import { StyledH1 } from 'components/headers';
import PlaylistSelector from './PlaylistSelector';


const PlaylistsPage = () => (
  <div>
    <StyledH1>Your Playlists</StyledH1>
    <PlaylistSelector />
  </div>
);

export default PlaylistsPage;
