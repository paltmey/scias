import React, {Component} from 'react';
import reactCSS from 'reactcss'
import Paper from 'material-ui/Paper';
import IconButton from 'material-ui/IconButton';
import ActionSearch from 'material-ui/svg-icons/action/search'
import {observable} from "mobx"
import {observer, inject} from 'mobx-react'

const styles = reactCSS({
    'default': {
        container: {
            flexBasis: '25%',
            height: '40px',
            lineHeight: '40px',
            margin: '8px 0px',
            paddingLeft: '16px',
            display: 'flex',
        },
        form: {
            flex: '1',
            display: 'flex'
        },
        input: {
            border: 'none',
            outline: 'none',
            flex: '1',
            fontSize: '16px',
        },
        button: {
            width: '40px',
            height: '40px',
            padding: '10px 8px 6px 8px',
            marginRight: '8px'
        }
    }
});

@inject("store")
@observer
class SearchField extends Component {

    @observable inputValue;

    constructor(props) {
        super(props);
        this.store = props.store.keyFrameStore;
        this.zDepth = props.zDepth;
        this.onSubmit = props.onSubmit;
        this.disableTouchRipple = props.disableTouchRipple;
        this.placeholder = props.placeholder;
        this.inputValue = ''
    }

    handleSubmit = (event) => {
        this.onSubmit(event, this.inputValue);
        event.preventDefault();
    };

    handleChange = (event) => {
        this.inputValue = event.target.value;
    };

    render() {
        return (
            <Paper
                zDepth={this.zDepth}
                style={styles.container}
            >
                <form onSubmit={this.handleSubmit} style={styles.form}>
                    <input style={styles.input} value={this.inputValue} placeholder={this.placeholder}
                           onChange={this.handleChange}/>
                </form>
                <IconButton disableTouchRipple={this.disableTouchRipple} style={styles.button} onTouchTap={this.handleSubmit}>
                    <ActionSearch />
                </IconButton>
            </Paper>
        )
    }
}
export default SearchField
