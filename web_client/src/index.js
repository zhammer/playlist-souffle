import React from 'react';
import ReactDOM from 'react-dom';
import Landing from 'scenes/Landing';

import { injectGlobal } from 'emotion';
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

ReactDOM.render(<Landing />, document.getElementById('root'));
