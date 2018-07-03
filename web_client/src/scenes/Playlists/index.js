import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { handlePlaylistSelected } from 'actions/ui';
import { getPlaylists } from 'selectors';
import PlaylistsPage from './PlaylistsPage';

const mapStateToProps = (state, props) => ({
  ...props,
  playlists: getPlaylists(state)
});

const mapDispatchToProps = dispatch => (
  bindActionCreators(
    {
      onPlaylistSelected: handlePlaylistSelected
    },
    dispatch
  )
);

export default connect(mapStateToProps, mapDispatchToProps)(PlaylistsPage);
