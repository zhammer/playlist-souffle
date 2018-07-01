import React, { Component } from 'react';
import { connect} from 'react-redux';
import { bindActionCreators } from 'redux';
import connectRouter from './components/connectRouter';
import { Redirect } from 'react-router';
import Landing from './Landing';
import { getAccessToken } from 'selectors';
import { handleAuthCodeReceived } from 'actions/auth';
import { redirectToAuthorizationPage } from 'services/api';

class LandingContainer extends Component {
  componentDidMount = () => {
    const { authCode } = this.props;
    if (authCode) {
      this.props.onAuthCodeReceived(authCode);
    }
  }

  render = () => (
    this.props.accessToken
      ? <Redirect to='/playlists'/>
      : <Landing onLoginButtonClicked={e => {e.preventDefault(); redirectToAuthorizationPage();}} />
  );
}


const mapQueryParamsToProps = ({ code }) => ({
  authCode: code
});

const ConnectedToRouter = connectRouter(mapQueryParamsToProps)(LandingContainer);

const mapStateToProps = (state, props) => (
  {
    accessToken: getAccessToken(state),
    ...props
  }
);

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      onAuthCodeReceived: handleAuthCodeReceived
    },
    dispatch
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(ConnectedToRouter);
