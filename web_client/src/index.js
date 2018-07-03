import React from 'react';
import ReactDOM from 'react-dom';
import { injectGlobal } from 'emotion';
import { Provider } from 'react-redux';
import colors from 'theme';
import store, { history } from './store';
import App from './App';

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



ReactDOM.render(
  <Provider store={store}>
    <App history={history} />
  </Provider>,
  document.getElementById('root'));
