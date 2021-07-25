function addSingleMarker(map, lnglat, color) {
    let timestamp = "Neko: " + neko++;
    var popup = new mapboxgl.Popup({ offset: 20, closeButton: false }).setText(timestamp);
    let marker = new mapboxgl.Marker({ color: color })
        .setLngLat(lnglat)
        .setPopup(popup)
        .addTo(map);
    return marker;
}
function addManyMarkers(map, lnglatlist, color = "blue") {
    var markerlist = [];
    for (const lnglat of lnglatlist) {
        var marker = addSingleMarker(map, lnglat, color);
        markerlist.push(marker);
    }
    return markerlist;
}
function asSrpMarker() {
    url = "http://localhost:8000/api/activitySegment.simplifiedRawPath"
    fetch(url, {
        mode: 'cors'
    })
        .then((response) => {
            return response.json();
        })
        .then((myjson) => {
            var asSrpMarkers = addManyMarkers(map, myjson["data"], "blue")
        })
        .catch((e) => {
            console.log(e);
        })
}
function asWpMarker() {
    url = "http://localhost:8000/api/activitySegment.waypointPath"
    fetch(url, {
        mode: 'cors'
    })
        .then((response) => {
            return response.json();
        })
        .then((myjson) => {
            var asWpMarkers = addManyMarkers(map, myjson["data"], "pink")
        })
        .catch((e) => {
            console.log(e);
        })
}
function pvSrpMarker() {
    url = "http://localhost:8000/api/placeVisit.simplifiedRawPath"
    fetch(url, {
        mode: 'cors'
    })
        .then((response) => {
            return response.json();
        })
        .then((myjson) => {
            var pvSrpMarkers = addManyMarkers(map, myjson["data"], "yellow")
        })
        .catch((e) => {
            console.log(e);
        })
}

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // マップのスタイル（デザイン）
    center: [-96, 37.8], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: 3 // 初期に表示する地図のズームレベル
});


var neko = 0;

const geojson = {
    "type": "FeatureCollection",
    "name": "sample",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": [
        {
            "type": "Feature",
            "properties": {
                "field01": "一",
                "field02": "abcd",
                "field03": 5
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    139.766778945922852,
                    35.68198003744061
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "field01": "二",
                "field02": null,
                "field03": 7
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    139.762916564941406,
                    35.674310750817348
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "field01": "三",
                "field02": "kojsha",
                "field03": 9
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    139.763603210449219,
                    35.691391336319306
                ]
            }
        }
    ]
}

map.on('load', function () {
    map.addSource('points', {
        'type': 'geojson',
        'data': geojson
    });
    map.addLayer({
        'id': 'point',
        'source': 'points',
        'type': 'circle',
        'paint': {
            'circle-radius': 10,
            'circle-color': '#007cbf'
        }
    });
});

//asSrpMarker();
//asWpMarker();
//pvSrpMarker();