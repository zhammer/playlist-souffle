import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getCurrentPlaylist, getCurrentPlaylistTracks } from 'selectors';
import SouffleStation from './SouffleStation';
import { handleSouffleStationLoaded } from './actions';

const mapStateToProps = (state, props) => ({
  ...props,
  playlist: getCurrentPlaylist(state)
});

export default connect(mapStateToProps)(SouffleStation);
