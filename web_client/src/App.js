import React, { Fragment } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Landing from 'scenes/Landing';
import { getAccessToken } from 'selectors';

const App = () => (
  <Router>
    <Fragment>
      <Route path='/' exact component={Landing}/>
    </Fragment>
  </Router>
);

export default App;
