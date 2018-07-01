import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getAccessToken } from 'selectors';
import { fetchPlaylists } from 'services/api';
import Playlists from './Playlists';

class PlaylistsContainer extends Component {
  componentDidMount = () => {
    const playlists = fetchPlaylists(this.props.accessToken);
    console.log(playlists);
  }

  render = () => (<Playlists />)
}


const mapStateToProps = (state, props) => ({
  ...props,
  accessToken: getAccessToken(state)
});


export default connect(mapStateToProps)(PlaylistsContainer);
