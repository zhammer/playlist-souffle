import { connect } from 'react-redux';
import { handlePlaylistSelected } from 'actions/ui';
import { handleLogoutButtonClicked } from 'actions/auth';
import { getPlaylists } from 'selectors';
import PlaylistsPage from './PlaylistsPage';

const mapStateToProps = (state, props) => ({
  ...props,
  playlists: getPlaylists(state)
});

const mapDispatchToProps = {
      onLogoutButtonClicked: handleLogoutButtonClicked,
      onPlaylistSelected: handlePlaylistSelected
};

export default connect(mapStateToProps, mapDispatchToProps)(PlaylistsPage);
