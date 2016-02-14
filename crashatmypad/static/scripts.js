if (document.fonts) {
    if (document.getElementById("main-page")) {
        document.getElementById("main-page").style.opacity = 0;
        document.fonts.ready.then(function () {
            document.getElementById("main-page").style.opacity = 1;
        });
    }
}

function calculateZoomForPoints(points) {
    return 13;
}


function getDisplayBoundsForPoints(points) {
    var xMin = 180;
    var xMax = -180;
    var yMin = 90;
    var yMax = -90;
    for (var i = 0; i < points.length; i++) {
        xMin = Math.min(xMin, points[i].longitude);
        xMax = Math.max(xMax, points[i].longitude);
        yMin = Math.min(yMin, points[i].latitude);
        yMax = Math.max(yMax, points[i].latitude);
    }

    return [
        [yMin, xMin],
        [yMax, xMax]
    ];
}

function getMaxBoundsFromInitialBounds(initialBounds) {
    return [
        [initialBounds._southWest.lat - 3, initialBounds._southWest.lng - 3],
        [initialBounds._northEast.lat + 3, initialBounds._northEast.lng + 3]
    ];
}

function getMapWithMarkers(points) {
    if (points.length > 0) {
        var firstMarker = points[0];
        var zoom = calculateZoomForPoints(points);
        var map = L.map('map');

        for (var i = 0; i < points.length; i++) {
            var marker = new L.circle([points[i].latitude, points[i].longitude], 200) // in m
                .addTo(map);
            var popup = new L.popup()
                .setLatLng([points[i].latitude, points[i].longitude])
                .setContent(points[i].user_name).addTo(map);
        }
        L.control.scale({position: 'topright'}).addTo(map);
        map.fitBounds(getDisplayBoundsForPoints(points), {padding: [10, 10]}); // in px
        var initialBounds = map.getBounds();
        map.setMaxBounds(getMaxBoundsFromInitialBounds(initialBounds));

        var osmUrl='https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png';
        var osmAttribution='Maps © <a href="http://www.thunderforest.com" target="_blank">Thunderforest</a>,' +
            ' Data © <a href="http://openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors';
        var osm = new L.tileLayer(osmUrl, {
            minZoom: 6,
            maxZoom: 14,
            attribution: osmAttribution
        });

        map.addLayer(osm);
    }
}