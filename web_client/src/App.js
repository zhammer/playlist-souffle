import React, { Component, Fragment } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { handleApplicationStarted } from 'actions/app';
import Landing from 'scenes/Landing';
import Playlists from 'scenes/Playlists';

const App = () => (
  <Router>
    <Fragment>
      <Route path='/' exact component={Landing}/>
      <Route path='/playlists' component={Playlists}/>
    </Fragment>
  </Router>
);

class AppContainer extends Component {
  componentDidMount = () => {
    this.props.onApplicationStarted();
  }

  render = () => (
    <App />
  )
}

const mapStateToProps = (state, props) => ({ ...props });

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      onApplicationStarted: handleApplicationStarted
    },
    dispatch
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(AppContainer);
