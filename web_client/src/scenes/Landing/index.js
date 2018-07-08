import React, { Component } from 'react';
import { connect} from 'react-redux';
import { Redirect } from 'react-router';
import Landing from './Landing';
import { getAccessToken } from 'selectors';
import { redirectToAuthorizationPage } from 'services/api';

class LandingContainer extends Component {
  render = () => (
    this.props.accessToken
      ? <Redirect to='/playlists'/>
      : <Landing onLoginButtonClicked={e => {e.preventDefault(); redirectToAuthorizationPage();}} />
  );
}

const mapStateToProps = (state, props) => (
  {
    accessToken: getAccessToken(state),
    ...props
  }
);

export default connect(mapStateToProps)(LandingContainer);
