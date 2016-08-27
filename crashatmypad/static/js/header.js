'use strict';
const qwest = require('qwest');

global.onLogout = function () {
    var location = document.location;
    console.log('location', location);
    qwest
        .delete('/session')
        .then(function (xhr, response) {
            console.log('Session deleted.', xhr, response);
            if (location) {
                document.location = location;
            } else {
                document.location = '/';
            }
        })
        .catch(function (e) {
            console.warn('Session delete failed', e);
        });
};
