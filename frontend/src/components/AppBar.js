import React, {Component} from 'react';
import {observer, inject} from 'mobx-react'
import Paper from 'material-ui/Paper';
import IconButton from 'material-ui/IconButton';
import FileUpload from 'material-ui/svg-icons/file/file-upload'
import {lightBlue300} from 'material-ui/styles/colors'
import reactCSS from 'reactcss'

import SearchField from './SearchField'
import views from '../config/views';

const styles = reactCSS({
    'default': {
        appBar: {
            backgroundColor: lightBlue300
        },
        buttonContainer: {
            display: 'flex',
            justifyContent: 'flex-end',
            alignItems: 'center',
            height: '100%'
        },
        button: {
            width: '28px',
            height: '28px',
            padding: '0'
        },
        icon: {
            width: '28px',
            height: '28px'
        }
    }
});

@inject("store")
@observer
class AppBar extends Component {

    constructor(props) {
        super(props);
        this.store = props.store.keyFrameStore;
        this.uiState = props.store.uiState;
        this.router = props.store.router;
    }

    handleSubmit = async (event, input) => {
        const res = await this.store.loadKeyFrames(input);

        if(res.ok) {
            this.router.goTo(views.home)
        }
    };

    handleUploadButtonClicked = () => {
        this.uiState.openUploadDialog();
    };

    render() {
        return (
            <div>
                <Paper className="row" style={styles.appBar}>
                    <div className="col-xs-offset-1 col-xs-3">
                        <div className="box">
                            <SearchField zDepth={2} disableTouchRipple={true} placeholder="Search"
                                         onSubmit={this.handleSubmit}/>
                        </div>
                    </div>
                    <div className="col-xs-offset-4 col-xs-1">
                        <div className="box" style={styles.buttonContainer}>
                            <IconButton disableTouchRipple={this.disableTouchRipple}
                                        style={styles.button}
                                        iconStyle={styles.icon}
                                        onTouchTap={this.handleUploadButtonClicked}
                            >
                                <FileUpload/>
                            </IconButton>
                        </div>
                    </div>

                </Paper>
            </div>
        );
    }
}

export default AppBar;
