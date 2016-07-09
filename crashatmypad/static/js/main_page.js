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
        .delete('/session', null, {
            responseType: 'document',
            headers: {
                'Access-Control-Allow-Origin': 'http://127.0.0.1:8000/'
            }
        })
        .then(function (xhr, response) {
            console.log('Session deleted.', xhr, response);
            // document.open();
            // document.write(xhr.response);
            // document.close();

        })
        .catch(function (e) {
            console.log('Session delete failed', e);
        });
};
