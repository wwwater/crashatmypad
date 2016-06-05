'use strict';

if (document.fonts) {
    if (document.getElementById('main-page')) {
        document.getElementById('main-page').style.opacity = 0;
        document.fonts.ready.then(function () {
            document.getElementById('main-page').style.opacity = 1;
        });
    }
}
