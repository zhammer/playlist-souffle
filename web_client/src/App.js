import React, { Component, Fragment } from 'react';
import { Route } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { ConnectedRouter } from 'connected-react-router';
import { handleApplicationStarted } from 'actions/app';
import { getLoading } from 'selectors';
import Loading from 'scenes/Loading';
import Landing from 'scenes/Landing';
import Playlists from 'scenes/Playlists';
import SouffleStation from 'scenes/SouffleStation';

const App = ({ history, loading }) => (
  loading ? <Loading /> :
  <ConnectedRouter history={history}>
    <Fragment>
      <Route path='/' exact component={Landing}/>
      <Route path='/playlists' exact component={Playlists}/>
      <Route path='/playlists/:id' component={SouffleStation}/>
    </Fragment>
  </ConnectedRouter>
);

class AppContainer extends Component {
  componentDidMount = () => {
    this.props.onApplicationStarted();
  }

  render = () => (
    <App {...this.props} />
  )
}

const mapStateToProps = (state, props) => ({
  ...props,
  loading: getLoading(state)
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      onApplicationStarted: handleApplicationStarted
    },
    dispatch
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(AppContainer);
