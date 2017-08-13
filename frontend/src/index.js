import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {Provider} from 'mobx-react'
import {RouterStore} from 'mobx-router';

import Frisbee from 'frisbee';

import injectTapEventPlugin from 'react-tap-event-plugin';

import KeyFrameStore from './stores/KeyFrameStore'
import UiState from './stores/UiState'
import App from './App';
import registerServiceWorker from './registerServiceWorker';

injectTapEventPlugin();

const api = new Frisbee({
    baseURI: process.env.NODE_ENV === 'production'
        ? 'http://localhost:8080'
        : 'http://localhost:3000',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
const keyFrameStore = new KeyFrameStore(api);
const uiState = new UiState();
const store = {
    keyFrameStore: keyFrameStore,
    uiState: uiState,
    router: new RouterStore()
};

ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);
registerServiceWorker();
