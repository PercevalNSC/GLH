function addSingleMarker(map, lnglat, color) {
    let timestamp = "Neko: " + neko++;
    var popup = new mapboxgl.Popup({ offset: 20, closeButton: false }).setText(timestamp);
    let marker = new mapboxgl.Marker({ color: color })
        .setLngLat(lnglat)
        .setPopup(popup)
        .addTo(map);
    return marker;
}
function addManyMarkers(map, lnglatlist, color="blue") {
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
function pvSrpMarker(){
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
    center: [139.5446, 35.6518], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: 13 // 初期に表示する地図のズームレベル
});

var neko = 0;

asSrpMarker();
asWpMarker();
pvSrpMarker();