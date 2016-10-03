'use strict';

var _ = require('lodash');
var requests = require('./requests');

function changeUser(event, userId, fieldName) {
    var value = event.target.value;
    console.log('New', fieldName, value);
    if (userId && fieldName && value) {
        requests.sendRequest('POST', '/user/' + userId +
                '?' + fieldName + '=' + value)
            .then(function () {
                console.log('User updated.');
            })
            .catch(function (err) {
                console.warn('User update failed', err);
            });
    } else {
        console.warn('Cannot update user. Need user id, the field name ' +
            'to update and a new value.');
    }
}

global.onUserChange = _.debounce(changeUser, 1000);
