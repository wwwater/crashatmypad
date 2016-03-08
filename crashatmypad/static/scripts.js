if (document.fonts) {
    if (document.getElementById("main-page")) {
        document.getElementById("main-page").style.opacity = 0;
        document.fonts.ready.then(function () {
            document.getElementById("main-page").style.opacity = 1;
        });
    }
}

// find minimal bounding box for locations that surround central point
function getDisplayBoundsForPoints(center, locations) {
    dxMax = 0
    dyMax = 0
    for (var i = 0; i < locations.length; i++) {
        dxMax = Math.max(dxMax, Math.abs(center.longitude - locations[i].longitude));
        dyMax = Math.max(dyMax, Math.abs(center.latitude - locations[i].latitude));
    }

    return [
        [center.latitude - dyMax, center.longitude - dxMax],
        [center.latitude + dyMax, center.longitude + dxMax]
    ];
}

function getMaxBoundsFromInitialBounds(initialBounds) {
    return [
        [initialBounds._southWest.lat - 3, initialBounds._southWest.lng - 3],
        [initialBounds._northEast.lat + 3, initialBounds._northEast.lng + 3]
    ];
}

function getMapWithMarkers(query, locations) {
    var map = L.map('map');
    L.control.scale({position: 'topright'}).addTo(map);
    L.marker([query.latitude, query.longitude]).addTo(map);

    for (var i = 0; i < locations.length; i++) {
        var marker = new L.circle([locations[i].latitude, locations[i].longitude], 200) // in m
            .addTo(map);
        var popup = new L.popup()
            .setLatLng([locations[i].latitude, locations[i].longitude])
            .setContent(locations[i].user_name).addTo(map);
    }

    map.fitBounds(getDisplayBoundsForPoints(query, locations), {padding: [10, 10]}); // in px

    if (locations.length > 0) {
        map.setZoom(Math.min(Math.max(map.getZoom(), 6), 14));
    } else {
        map.setZoom(10);
    }

    map.setMaxBounds(getMaxBoundsFromInitialBounds(map.getBounds()));

    var tileUrl='https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png';
    var attribution='Maps © <a href="http://www.thunderforest.com" target="_blank">Thunderforest</a>,' +
        ' Data © <a href="http://openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors';

    var osm = new L.tileLayer(tileUrl, {
        minZoom: 6,
        maxZoom: 14,
        attribution: attribution
    });

    map.addLayer(osm);
}