import React, { Fragment } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
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

export default App;
