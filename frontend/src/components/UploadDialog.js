import React, {Component} from 'react';
import {observer, inject} from 'mobx-react'
import Dialog from 'material-ui/Dialog';
import DropzoneComponent from 'react-dropzone-component';

import 'react-dropzone-component/styles/filepicker.css';
import 'dropzone/dist/min/dropzone.min.css';

const componentConfig = {
    iconFiletypes: ['.jpg', '.png', '.mp4'],
    showFiletypeIcon: true,
    postUrl: '/uploadHandler'
};

@inject("store")
@observer
class UploadDialog extends Component {

    constructor(props) {
        super(props);
        this.uiState = props.store.uiState;
    }

    handleClose = () => {
        this.uiState.closeUploadDialog()
    };

    render() {
        return (
            <Dialog
                title="Dialog With Actions"
                modal={false}
                open={this.uiState.uploadDialogOpen}
                onRequestClose={this.handleClose}
            >
                <DropzoneComponent config={componentConfig}/>
            </Dialog>
        );
    }
}

export default UploadDialog;
