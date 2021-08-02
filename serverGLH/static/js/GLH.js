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
function dbPoint(url, id, color, radius = 4, opacity = 0.65) {
    fetch(url, {
        mode: 'cors'
    }).then((response) => {
        return response.json();
    }).then((geojson) => {
        map.addSource(id, {
            'type': 'geojson',
            'data': geojson
        });
        map.addLayer({
            'id': id,
            'source': id,
            'type': 'circle',
            'paint': {
                'circle-radius': radius,
                'circle-opacity': opacity,
                'circle-color': color,
                'circle-stroke-width': 1
            }
        });
    }).catch((e) => {
        console.log(e);
    });

    map.on('click', id, function(e){
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = "Timestamp:" + e.features[0].properties.timestamp;
        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    });
}
function asSrpPoint() {
    url = "http://localhost:8000/api/geojson/activitySegment.simplifiedRawPath"
    dbPoint(url, "asSrp", "blue");
}
function asWpPoint() {
    url = "http://localhost:8000/api/geojson/activitySegment.waypointPath"
    dbPoint(url, "asWp", "pink");
}
function pvSrpPoint() {
    url = "http://localhost:8000/api/geojson/placeVisit.simplifiedRawPath"
    dbPoint(url, "pvSrp", "yellow");
}
function pvLocationPoint() {
    url = "http://localhost:8000/api/geojson/placeVisit.location"
    dbPoint(url, "pvLocation", "white", radius = 6, opacity = 0.5);
}

//

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // マップのスタイル（デザイン）
    center: [139.56, 35.65], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: 13, // 初期に表示する地図のズームレベル
});

map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());
//map.addControl(new mapboxgl.ScaleControl());

map.on('load', function () {
    pvLocationPoint();
    asSrpPoint();
    asWpPoint();
    pvSrpPoint();
});