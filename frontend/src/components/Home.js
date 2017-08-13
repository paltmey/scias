import React, {Component} from 'react';
import {observer, inject} from 'mobx-react'
import {lightBlue300} from 'material-ui/styles/colors'
import reactCSS from 'reactcss'

import PredictionList from './PredictionList'
import KeyFrameList from './KeyFrameList'

const styles = reactCSS({
    'default': {
        appBar: {
            backgroundColor: lightBlue300
        },
        content: {
            margin: '16px 0px'
        },

        keyFrameList: {}
    }
});

@inject("store")
@observer
class Home extends Component {

    constructor(props) {
        super(props);
        this.store = props.store.keyFrameStore;
    }

    render() {
        return (
            <div className="row" style={styles.content}>
                <div className="col-xs-offset-1 col-xs-8">
                    <div className="box">
                        <KeyFrameList style={styles.keyFrameList}/>
                    </div>
                </div>
                {this.store.keyFrames.length > 0 &&
                <div className="col-xs-2">
                    <div className="box">
                        <PredictionList/>
                    </div>
                </div>
                }
            </div>
        );
    }
}

export default Home;
