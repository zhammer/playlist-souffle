import React, { Component, Fragment } from 'react';
import { Route } from 'react-router-dom';
import { connect } from 'react-redux';
import { ConnectedRouter } from 'connected-react-router';
import { handleApplicationStarted } from 'actions/app';
import { getLoading } from 'selectors';
import withLoading from 'components/withLoading';
import Loading from 'scenes/Loading';
import Landing from 'scenes/Landing';
import Playlists from 'scenes/Playlists';
import SouffleStation from 'scenes/SouffleStation';

const App = ({ history }) => (
  <ConnectedRouter history={history}>
    <Fragment>
      <Route path='/' exact component={Landing}/>
      <Route path='/playlists' exact component={Playlists}/>
      <Route path='/playlists/:id' component={SouffleStation}/>
    </Fragment>
  </ConnectedRouter>
);

const AppWithLoading = withLoading(App, Loading);

class AppContainer extends Component {
  componentDidMount = () => {
    this.props.onApplicationStarted();
  }

  render = () => (
    <AppWithLoading {...this.props} />
  )
}

const mapStateToProps = (state, props) => ({
  ...props,
  loading: getLoading(state)
});

const mapDispatchToProps = {
  onApplicationStarted: handleApplicationStarted
};

export default connect(mapStateToProps, mapDispatchToProps)(AppContainer);
