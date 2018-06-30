import React, { Fragment } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Landing from 'scenes/Landing';

const App = () => (
  <Router>
    <Fragment>
      <Route path='/' exact component={Landing}/>
    </Fragment>
  </Router>
);

export default App;
