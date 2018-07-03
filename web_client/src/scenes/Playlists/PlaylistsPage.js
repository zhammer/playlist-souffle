import React from 'react';
import { StyledH1 } from 'components/headers';
import PlaylistsGrid from './PlaylistsGrid';


const PlaylistsPage = () => (
  <div>
    <StyledH1>Your Playlists</StyledH1>
    <PlaylistsGrid />
  </div>
);

export default PlaylistsPage;
