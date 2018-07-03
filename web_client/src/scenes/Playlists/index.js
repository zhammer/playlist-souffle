import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { handlePlaylistsPageLoaded, handlePlaylistSelected } from 'actions/playlists';
import { getPlaylists } from 'selectors';
import PlaylistsPage from './PlaylistsPage';

class PlaylistsPageContainer extends Component {
  componentDidMount = () => {
    this.props.onPlaylistsPageLoaded();
  }

  render = () => (
    <PlaylistsPage
      playlists={this.props.playlists}
      onPlaylistSelected={this.props.onPlaylistSelected}
      />
  )
}

const mapStateToProps = (state, props) => ({
  ...props,
  playlists: getPlaylists(state)
});


const mapDispatchToProps = dispatch => (
  bindActionCreators(
    {
      onPlaylistsPageLoaded: handlePlaylistsPageLoaded,
      onPlaylistSelected: handlePlaylistSelected
    },
    dispatch
  )
);


export default connect(mapStateToProps, mapDispatchToProps)(PlaylistsPageContainer);
