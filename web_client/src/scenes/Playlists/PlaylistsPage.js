import React from 'react';
import { StyledH1 } from 'components/headers';
import PlaylistsGrid from './PlaylistsGrid';


const PlaylistsPage = ({ playlists, onPlaylistSelected }) => (
  <div>
    <StyledH1>Your Playlists</StyledH1>
    <PlaylistsGrid
      onPlaylistSelected={onPlaylistSelected}
      playlists={playlists}
      />
  </div>
);

export default PlaylistsPage;
