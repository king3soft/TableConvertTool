import React from 'react';
import ReactDOM from 'react-dom';

import App from "./app";

console.log("ui.js", window.console);
window.console.debug = (...args) => {}


ReactDOM.render(
        <App />
, document.querySelector('#container'));