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

class DrawStructure {
    constructor(url, id, color, opacity, visibility){
        this.url = url;
        this.id = id;
        this.color = color;
        this.opacity = opacity;
        this.visibility = visibility;
    }
    add_structure(){
        fetch(url, {
            mode: 'cors'
        }).then((response) => {
            return response.json();
        }).then((geojson) => {
            this._add_geojson(geojson)
            console.log("Write: " + this.url);
        }).catch((e) => {
            console.log(e);
        });
    }
    _add_geojson(geojson){
        this._add_source(geojson);
        this._add_layer();

    }
    _add_source(geojson){
        map.addSource(this.id, {
            'type': 'geojson',
            'data': geojson
        });
    }
    _add_layer(){
        // specified structure
        map.addLayer({
            'id': this.id,
            'source': this.id,
            'type': 'circle',
            'layout': {
                'visibility': this.visibility
            },
            'paint': {},
        });
    }
}

class DrawPoints extends DrawStructure{
    constructor(url, id, color = 'black', radius = 4, opacity = 1.0, visibility = 'visible'){
        super(url, id, color, opacity, visibility);
        this.radius = radius
    }
    _add_layer(){
        map.addLayer({
            'id': this.id,
            'source': this.id,
            'type': 'circle',
            'layout': {
                'visibility': this.visibility
            },
            'paint': {
                'circle-radius': this.radius,
                'circle-opacity': this.opacity,
                'circle-color': this.color,
                'circle-stroke-width': 1
            }
        });
        this._click_popup();
    }
    _click_popup(){
        map.on('click', this.id, function (e) {
            var coordinates = e.features[0].geometry.coordinates.slice();
            var date = new Date(e.features[0].properties.timestamp)
            var description = "Timestamp:" + date.toString();
            new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
        });
    }
}
function asSrpPoint() {
    url = "http://localhost:8000/api/geojson/point/activitySegment.simplifiedRawPath"
    let as_srp_point = new DrawPoints(url, "AsSrp", color = "blue")
    as_srp_point.add_structure();
}
function asWpPoint() {
    url = "http://localhost:8000/api/geojson/point/activitySegment.waypointPath"
    let as_wp_point = new DrawPoints(url, "AsWp", color = "pink")
    as_wp_point.add_structure();
}
function pvSrpPoint() {
    url = "http://localhost:8000/api/geojson/point/placeVisit.simplifiedRawPath"
    let pv_srp_point = new DrawPoints(url, "PvSrp", color = "yellow");
    pv_srp_point.add_structure();
}
function pvLocationPoint() {
    url = "http://localhost:8000/api/geojson/point/placeVisit.location"
    let pv_location = new DrawPoints(url, "PvLoc", color = "white", radius = 6, opacity = 1);
    pv_location.add_structure();
}
function dbscanPoint() {
    url = "http://localhost:8000/api/geojson/point/dbscan"
    let dbscan_point = new DrawPoints(url, "dbscan_point");
    dbscan_point.add_structure();
}
class DrawLine extends DrawStructure {
    constructor(url, id, color = 'black', width = 1, opacity = 0.5, visibility = 'visible'){
        super(url, id, color, opacity, visibility);
        this.witdh = width
    }
    _add_layer(){
        map.addLayer({
            'id': this.id,
            'type': 'line',
            'source': this.id,
            'layout': {
                'line-join': 'bevel',
                'line-cap': 'butt'
            },
            'paint': {
                'line-color': this.color,
                'line-opacity': this.opacity,
                'line-width': this.witdh
            }
        });
    }
}

function add_routepath(color = '#888', opacity = 0.5, width = 1){
    url = "http://localhost:8000/api/geojson/line/route"
    id = "routepath"
    let routepath = new DrawLine(url, id, color, width, opacity);
    routepath.add_structure();
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
function optics_polygon() {
    url = "http://localhost:8000/api/geojson/polygon/optics"
    id = "optics_polygon"
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

    add_routepath();
    asWpPoint();
    asSrpPoint();
    pvSrpPoint();
    pvLocationPoint();
    //dbscanPoint();
    //dbscan_polygon();
    //optics_polygon();
});