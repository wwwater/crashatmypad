'use strict';
const qwest = require('qwest');

if (document.fonts) {
    var fonts = new FontFace('fonts', 'url(https://fonts.googleapis.com/css?' +
        'family=Overlock:400,700|Cabin+Sketch:700)');
    document.fonts.add(fonts);
    if (document.getElementById('main-page')) {
        document.getElementById('main-page').style.opacity = 0;
        document.fonts.onloadingdone = function () {
            document.getElementById('main-page').style.opacity = 1;
        };
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
