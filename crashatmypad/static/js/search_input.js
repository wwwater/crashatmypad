'use strict';

var _ = require('lodash');

var searchInput = document.getElementById('input-location');
if (searchInput) {
    searchInput.setAttribute('autocomplete', 'off');
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

function getOptionClassName(i) {
    return 'option-city' + (i % 2 === 0 ? ' another' : '');
}

function goToSearchPage(fullName) {
    window.location.href = 'location?q=' + fullName;
}

function onKeyDownCitySelector(number, fullName, event) {
    if (event.keyCode === 38) { // arrow up
        event.stopPropagation();
        event.preventDefault();
        var selector = document.getElementById('selector-city');
        if (number === 0) {
            var input = document.getElementById('input-location');
            input.focus();

        } else {
            var prevOption = selector.children[number - 1];
            prevOption.className = 'option-city selected';
            prevOption.focus();
        }
        selector.children[number].className = getOptionClassName(number);
    } else if (event.keyCode === 40) { // arrow down
        var selector = document.getElementById('selector-city');
        var nextOption = selector.children[number + 1];
        if (nextOption) {
            nextOption.className = 'option-city selected';
            nextOption.focus();
            selector.children[number].className = getOptionClassName(number);
        }
    } else if (event.keyCode === 13) { // enter
        goToSearchPage(fullName);
    } else if (event.keyCode >= 48 && event.keyCode <= 90) { // alfanum
        var input = document.getElementById('input-location');
        input.focus();
        input.oninput({target: {value: input.value + event.key}});
    } else if (event.keyCode === 8) { // backspace
        var input = document.getElementById('input-location');
        input.focus();
        input.oninput({target: {
            value: input.value.substring(0, input.value.length - 1)
        }});
    }
}

global.onChangeSearchInput = function (event) {
    var query = event.target.value;
    console.log('on search input change', query);
    if (query.length > 2) {
        sendRequest('GET', 'city?q=' + query)
        .then(function (data) {
            var selector = document.getElementById('selector-city');

            while (selector.firstChild) {
                selector.removeChild(selector.firstChild);
            }

            var cities = JSON.parse(data).cities;
            console.log('Got cities', cities);
            var nOptions = Math.min(cities.length, 10);
            for (var i = 0; i < nOptions; i++) {
                var option = document.createElement('div');
                var fullName = _.join(
                    [cities[i].city, cities[i].state, cities[i].country], ',');
                option.innerText = cities[i].city + ' (' + cities[i].state +
                    '), ' + cities[i].country;
                option.className = getOptionClassName(i);
                option.tabIndex = '-1';
                option.addEventListener('click',
                    goToSearchPage.bind(null, fullName), false);
                option.addEventListener('keydown',
                    onKeyDownCitySelector.bind(null, i, fullName), true);
                selector.appendChild(option);
            }
        })
        .catch(function (data) {
            console.log('Failed getting cities', data);
        });
    } else {
        var selector = document.getElementById('selector-city');
        if (selector) {
            while (selector.firstChild) {
                selector.removeChild(selector.firstChild);
            }
        }
    }
};

global.onKeyDownSearchInput = function (event) {
    if (event.keyCode === 40) { // arrow down
        var selector = document.getElementById('selector-city');
        if (selector.firstChild) {
            selector.firstChild.className = 'option-city selected';
            selector.firstChild.focus();
        }
    }
};



