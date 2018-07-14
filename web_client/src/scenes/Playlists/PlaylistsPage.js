import React from 'react';
import styled from 'react-emotion';
import { StyledH1 } from 'components/headers';
import { DangerButton } from 'components/buttons';
import PlaylistsGrid from './PlaylistsGrid';

const ButtonContainer = styled('div')`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2em;
`;


const PlaylistsPage = ({ playlists, onPlaylistSelected, onLogoutButtonClicked }) => (
  <div>
    <StyledH1>Your Playlists</StyledH1>
    <PlaylistsGrid
      onPlaylistSelected={onPlaylistSelected}
      playlists={playlists}
      />
    <ButtonContainer>
      <DangerButton onClick={onLogoutButtonClicked}>Logout</DangerButton>
    </ButtonContainer>
  </div>
);

export default PlaylistsPage;
