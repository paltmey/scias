import React, {Component} from 'react';
import {observer, inject} from 'mobx-react'
import Paper from 'material-ui/Paper';
import reactCSS from 'reactcss'

const styles = reactCSS({
    'default': {
        row: {
            display: 'flex',
            justifyContent: 'center'
        },
        video: {
            display: 'block',
            width: '100%'
        },
        videoContainer: {
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
        this.router = props.store.router;
        this.video = props.store.router.queryParams.v;
        this.time = props.store.router.queryParams.t;
        this.autoPlay = this.time === undefined;
    }

    get srcString() {
        let src = `/videos/${this.video}.mp4`;

        if(this.time) {
            src += `#t=${this.time}`
        }
        return src;
    };

    render() {
        return (
            <div className="row">
                <div className="col-xs-offset-1 col-xs-7">
                    <Paper className="box" style={styles.videoContainer} zDepth={2}>
                        <video
                            controls
                            autoPlay = {this.autoPlay}
                            style={styles.video}
                            >
                            <source src={this.srcString} type="video/mp4" />
                        </video>
                    </Paper>
                </div>
            </div>
        );
    }
}

export default Home;
