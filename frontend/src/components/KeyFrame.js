import React, {Component} from 'react';
import reactCSS from 'reactcss'
import {observer, inject} from 'mobx-react'
import {Link} from 'mobx-router'

import views from '../config/views';

const styles = reactCSS({
    'default': {
        image: {
            width: '240px',
            margin: '0px 4px 4px 4px'
        }
    }
});

@inject("store")
@observer
class KeyFrame extends Component {

    constructor(props) {
        super(props);
        this.store = props.store;
        this.keyFrame = props.keyFrame;
    }

    render() {
        return (
            <Link view={views.player} store={this.store} queryParams={{'v':this.keyFrame.video_id, 't':this.keyFrame.time}}>
                <img key={this.keyFrame}
                     src={this.keyFrame.thumbnail}
                     title={this.keyFrame.weighted_score_sum}
                     style={styles.image}
                     alt=""
                />
            </Link>
        )
    }
}

export default KeyFrame;