'use strict';
const qwest = require('qwest');

if (document.fonts) {
    if (document.getElementById('main-page')) {
        document.getElementById('main-page').style.opacity = 0;
        document.fonts.ready.then(function () {
            document.getElementById('main-page').style.opacity = 1;
        });
    }
}

global.onLogout = function () {
    qwest
        .delete('/session')
        .then(function (xhr, response) {
            console.log('Session deleted.', xhr, response);
            document.location = '/';
        })
        .catch(function (e) {
            console.warn('Session delete failed', e);
        });
};
