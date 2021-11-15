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
        console.log("Write: " + url);
    }).catch((e) => {
        console.log(e);
    });

    map.on('click', id, function (e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var date = new Date(e.features[0].properties.timestamp)
        var description = "Timestamp:" + date.toString();
        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    });
}
function asSrpPoint() {
    url = "http://localhost:8000/api/geojson/point/activitySegment.simplifiedRawPath"
    dbPoint(url, "asSrp", "blue");
}
function asWpPoint() {
    url = "http://localhost:8000/api/geojson/point/activitySegment.waypointPath"
    dbPoint(url, "asWp", "pink");
}
function pvSrpPoint() {
    url = "http://localhost:8000/api/geojson/point/placeVisit.simplifiedRawPath"
    dbPoint(url, "pvSrp", "yellow");
}
function pvLocationPoint() {
    url = "http://localhost:8000/api/geojson/point/placeVisit.location"
    dbPoint(url, "pvLocation", "white", radius = 6, opacity = 1);
}
function dbscanPoint() {
    url = "http://localhost:8000/api/geojson/point/dbscan"
    dbPoint(url, "dbscan", "red", radius = 10, opacity = 0.5);
}
function dbline(color = '#888', opacity = 0.5, witdh = 1) {
    url = "http://localhost:8000/api/geojson/line"
    id = "routepath"
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
            'type': 'line',
            'source': id,
            'layout': {
                'line-join': 'bevel',
                'line-cap': 'butt'
            },
            'paint': {
                'line-color': color,
                'line-opacity': opacity,
                'line-width': witdh
            }
        });
        console.log("Write: " + url);
    }).catch((e) => {
        console.log(e);
    });
}
function db_polygon(url, id, fillcolor = '#0080ff') {
    fetch(url, {
        mode: 'cors'
    }).then((response) => {
        return response.json();
    }).then((geojson) => {
        add_db_polygon(id, geojson, fillcolor);
        console.log("Write: " + url);
    }).catch((e) => {
        console.log(e);
    });
};
function add_db_polygon(id, data, fillcolor = '#0080ff') {
    map.addSource(id, {
        'type': 'geojson',
        'data': data
    });
    //polygon_fill(id, fillcolor);
    polygon_sorround(id);
}
function polygon_fill(id, fillcolor = '#0080ff'){
    map.addLayer({
        'id': id + "fill",
        'type': 'fill',
        'source': id, // reference the data source
        'layout': {},
        'paint': {
            'fill-color': fillcolor, // blue color fill
            'fill-opacity': 0.5
        }
    });
}
function polygon_sorround(id){
    map.addLayer({
        'id': id + "outline",
        'type': 'line',
        'source': id,
        'layout': {},
        'paint': {
            'line-color': '#000',
            'line-width': 3
        }
    })
}
function dbscan_polygon() {
    url = "http://localhost:8000/api/geojson/polygon/dbscan"
    id = "dbscan_polygon"
    db_polygon(url, id)
}
//

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [139.56, 35.65], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: 13, // 初期に表示する地図のズームレベル
});

map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());
//map.addControl(new mapboxgl.ScaleControl());

map.on('load', function () {
    //dbline('#888', 0.5, 1);

    //asWpPoint();
    asSrpPoint();
    pvSrpPoint();
    //pvLocationPoint();
    //dbscanPoint();
    dbscan_polygon();
});