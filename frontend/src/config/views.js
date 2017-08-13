import React from 'react';
import {Route} from 'mobx-router';

import Home from '../components/Home'
import Player from '../components/Player'

const views = {
    home: new Route({
        path: '/',
        component: <Home/>
    }),
    player: new Route({
        path: '/watch',
        component: <Player/>
    })
};

export default views;