import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { getCurrentPlaylist } from 'selectors';
import SouffleStation from './SouffleStation';
import { handleSouffleStationLoaded } from './actions';

class SouffleStationContainer extends Component {
  componentDidMount = () => {
    this.props.onSouffleStationLoaded();
  }

  render = () => <SouffleStation {...this.props} />
}

const mapStateToProps = (state, props) => ({
  ...props,
  playlist: getCurrentPlaylist(state)
});

const mapDispatchToProps = dispatch => (
  bindActionCreators(
    {
      onSouffleStationLoaded: handleSouffleStationLoaded
    },
    dispatch
  )
);


export default connect(mapStateToProps, mapDispatchToProps)(SouffleStationContainer);
