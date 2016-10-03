'use strict';

exports.sendRequest = function (type, url) {
    return new Promise(function (resolve, reject) {
        var request = new XMLHttpRequest();
        request.open(type, url);
        request.send();
        request.onload = function () {
            if (this.status >= 200 && this.status < 400) {
                // Performs the function 'resolve' when this.status is equal to [23]xx
                resolve(this.response);
            } else {
                // Performs the function 'reject' when this.status is different than [23]xx
                reject(this.statusText);
            }
        };
        request.onerror = function () {
            reject(this.statusText);
        };
    });
};
