'use strict';

var _ = require('lodash');
console.log(_.map([1, 2, 3], function (n) { return n + ' meow'; }));

var searchInput = document.getElementById('input-location');
if (searchInput) {
    searchInput.setAttribute('autocomplete', 'off');
}

var selector = document.getElementById('selector-city');
if (selector) {
    selector.size = 0;
    selector.style.height = 0;
}


function sendRequest(type, url) {
    return new Promise(function (resolve, reject) {
        var request = new XMLHttpRequest();
        request.open(type, url);
        request.send();
        request.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                // Performs the function 'resolve' when this.status is equal to 2xx
                resolve(this.response);
            } else {
                // Performs the function 'reject' when this.status is different than 2xx
                reject(this.statusText);
            }
        };
        request.onerror = function () {
            reject(this.statusText);
        };
    });
}

global.onChangeSearchInput = function (event) {
    var query = event.target.value;
    console.log('on search input change', query);
    if (query.length > 0) {
        sendRequest('GET', 'city?q=' + query)
        .then(function (data) {
            selector = document.getElementById('selector-city');

            while (selector.firstChild) {
                selector.removeChild(selector.firstChild);
            }

            var cities = JSON.parse(data).cities;
            console.log('Got cities', cities);
            var nOptions = Math.min(cities.length, 10);
            if (nOptions > 0) {
                // when only 1 option set the size to 2 to avoid collapsing
                selector.size = Math.max(nOptions, 2);
                for (var i = 0; i < nOptions; i++) {
                    var option = document.createElement('option');
                    option.value = cities[i].city + ',' + cities[i].state +
                        ',' + cities[i].country;
                    option.text = cities[i].city + ' (' + cities[i].state +
                        '), ' + cities[i].country;
                    option.className = 'option-city';
                    selector.appendChild(option);
                    console.log('Append option with', option.value);
                }
            }
            selector.style.height = (nOptions * 29) + 'px';
        })
        .catch(function (data) {
            console.log('Failed getting cities', data);
        });
    } else {
        selector = document.getElementById('selector-city');
        if (selector) {
            selector.size = 0;
            selector.style.height = 0;
        }
    }
};

global.onKeyDownSearchInput = function (event) {
    if (event.keyCode === 40) { // arrow down
        selector = document.getElementById('selector-city');
        if (selector.firstChild) {
            selector.options[0].selected = true;
            selector.focus();
        }
    }

};

global.onKeyDownCitySelector = function (event) {
    if (event.keyCode === 38) { // arrow up
        selector = document.getElementById('selector-city');
        if (selector.selectedIndex === 0) {
            var input = document.getElementById('input-location');
            input.focus();
        }
    } else if (event.keyCode === 13) { // enter
        selector = document.getElementById('selector-city');
        var query = selector.options[selector.selectedIndex].value;
        window.location.href = 'location?q=' + query;
    }
};

global.onDoubleClickCitySelector = function () {
    selector = document.getElementById('selector-city');
    var query = selector.options[selector.selectedIndex].value;
    console.log('on double click city', query);
    window.location.href = 'location?q=' + query;
};
