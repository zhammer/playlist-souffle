import React from 'react';
import ReactDOM from 'react-dom';
import { injectGlobal } from 'emotion';
import { createStore, applyMiddleware, compose } from 'redux';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk';
import App from './App';
import reducers from 'reducers';
import colors from 'theme';

injectGlobal`
  * {
    box-sizing: border-box;
  }
  @import url('https://fonts.googleapis.com/css?family=Monoton|Quicksand');

  body {
    margin: 0;
    padding: 0;
    font-family: 'Quicksand', sans-serif;
    background-color: ${colors.darkBlue};
  }
`;

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(reducers, composeEnhancers(applyMiddleware(thunk)));

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root'));
