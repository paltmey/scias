import React, {Component} from 'react';
import {observer, inject} from 'mobx-react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {MobxRouter, startRouter} from 'mobx-router';

import DevTools from 'mobx-react-devtools';

import AppBar from './components/AppBar'
import UploadDialog from './components/UploadDialog'
import views from './config/views';

@inject("store")
@observer
class App extends Component {

    constructor(props) {
        super(props);
        startRouter(views, props.store)
    }

    render() {
        return (
            <div className="App">
                <MuiThemeProvider>
                    <div>
                        <AppBar/>
                        <UploadDialog/>
                        <MobxRouter/>
                    </div>
                </MuiThemeProvider>
                {process.env.NODE_ENV !== 'production' &&
                    <DevTools/>
                }
            </div>

        );
    }
}

export default App;
