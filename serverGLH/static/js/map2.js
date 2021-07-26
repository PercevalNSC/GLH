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
function dbPoint(url, id, color) {
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
                'circle-radius': 4,
                'circle-color': color
            }
        });
    }).catch((e) => {
        console.log(e);
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
    dbPoint(url, "pvSrp", "purple");
}

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // マップのスタイル（デザイン）
    center: [139.56, 35.65], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: 10 // 初期に表示する地図のズームレベル
});


var neko = 0;

map.on('load', function () {
    asSrpPoint();
    asWpPoint();
    pvSrpPoint();
});