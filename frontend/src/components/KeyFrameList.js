import React, {Component} from 'react';
import Paper from 'material-ui/Paper';
import reactCSS from 'reactcss'
import {observer, inject} from 'mobx-react'
import UltimatePaginationMaterialUi from 'react-ultimate-pagination-material-ui'

import KeyFrame from './KeyFrame'

const styles = reactCSS({
    'default': {
        background: {
            overflow: 'auto',
            padding: '16px 12px',
            minHeight: '200px',
            display: 'flex',
            flexDirection: 'column'
        },
        image: {
            width: '240px',
            margin: '0px 4px 4px 4px'
        },
        pagination: {
            margin: 'auto auto 0 auto',
            paddingTop: '6px'
        }
    }
});

@inject("store")
@observer
class KeyFrameList extends Component {

    constructor(props) {
        super(props);
        this.store = props.store.keyFrameStore;
    }

    handleChange = (page) => {
        this.store.loadKeyFrames(this.store.lastQuery, page - 1);
    };

    render() {
        const keyFrames = this.store.keyFrames.map((keyFrame) => <KeyFrame key={keyFrame.key_frame_id} keyFrame={keyFrame}/>);

        return (
            <Paper style={styles.background}>
                <div>
                    {keyFrames}
                </div>
                <div style={styles.pagination}>
                    <UltimatePaginationMaterialUi currentPage={this.store.currentPage+1}
                                                  totalPages={this.store.totalPages} onChange={this.handleChange}/>
                </div>
            </Paper>
        )
    }
}

export default KeyFrameList;