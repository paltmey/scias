import React, {Component} from 'react';
import Paper from 'material-ui/Paper';
import Divider from 'material-ui/Divider';
import reactCSS from 'reactcss'
import {observer, inject} from 'mobx-react'

const styles = reactCSS({
    'default': {
        list: {
            padding: '8px 0px',
            boxSizing: 'border-box'
        },
        listItem: {
            width: '240px',
            margin: '4px'
        },
        firstString: {
            fontSize: '16px'
        },
        rest: {
            fontSize: '12px',
        },
        entry: {
            display: 'flex',
            margin: '8px 16px 8px 16px'
        },
        divider: {
            marginTop: '8px'
        },
        humanString: {
            flex: 1,
            textAlign: 'left'
        },
        weight: {
            textAlign: 'right',
            marginLeft: '16px'
        }
    }
});

@inject("store")
@observer
class PredictionList extends Component {

    constructor(props) {
        super(props);
        this.store = props.store.keyFrameStore;
    }

    render() {
        const predictions = this.store.labeledPredictions.map(function (prediction, i) {
            const split = prediction.human_string.split(',');
            const first_string = split.pop();
            const rest = split.join();

            return (
                <div key={prediction.node}>
                    {i > 0 && <Divider style={styles.divider}/> }
                    <div style={styles.entry}>
                        <div style={styles.humanString}>
                            <span style={styles.firstString}>{first_string}</span>
                            {rest && <span style={styles.rest}>, {rest}</span>}
                        </div>
                        <div style={styles.weight}>{prediction.weight}</div>
                    </div>
                </div>
            )
        });

        return (
            <Paper style={styles.list}>
                {predictions}
            </Paper>

        )
    }
}

export default PredictionList;