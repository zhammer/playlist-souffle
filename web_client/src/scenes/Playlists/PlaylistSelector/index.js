import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { getAccessToken } from 'selectors';
import { fetchPlaylists } from 'services/api';
import { handlePlaylistsPageLoaded } from './actions';
import { getPlaylists, getPlaylistsPageLoading } from './selectors';
import Playlists from './Playlists';

class PlaylistsContainer extends Component {
  componentDidMount = () => {
    this.props.onPlaylistsPageLoaded();
  }

  render = () => (<Playlists playlists={this.props.playlists}/>)
}


const mapStateToProps = (state, props) => ({
  ...props,
  accessToken: getAccessToken(state),
  playlists: getPlaylists(state),
  loading: getPlaylistsPageLoading(state)
});


const mapDispatchToProps = dispatch => (
  bindActionCreators(
    {
      onPlaylistsPageLoaded: handlePlaylistsPageLoaded
    },
    dispatch
  )
);


export default connect(mapStateToProps, mapDispatchToProps)(PlaylistsContainer);
