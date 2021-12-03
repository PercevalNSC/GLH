centers = {"chofu": [139.545, 35.655]};
init_zoom = 15;
neko = 0

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
function dbscan_point() {
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

function add_routepath(color = 'gray', opacity = 0.5, width = 1){
    url = "http://localhost:8000/api/geojson/line/route"
    id = "routepath"
    let routepath = new DrawLine(url, id, color, width, opacity);
    routepath.add_structure();
}

class DrawPolygon extends DrawStructure {
    constructor(url, id, fillcolor = "white", linecolor = "black", width = 3, opacity = 0.5, visibility = "visivle"){
        super(url, id, fillcolor, opacity, visibility);
        this.linecolor = linecolor;
        this.width = width;
    }
    _add_layer(){
        if (this.color != "None") {
            this._add_fill_layer();
        };
        this._add_surround_layer();
    }
    _add_fill_layer(){
        map.addLayer({
            'id': this.id + "fill",
            'type': 'fill',
            'source': this.id, // reference the data source
            'layout': {},
            'paint': {
                'fill-color': this.color, // blue color fill
                'fill-opacity': this.opacity
            }
        });
    }
    _add_surround_layer(){
        console.log(this.id + "outline")
        map.addLayer({
            'id': this.id + "outline",
            'type': 'line',
            'source': this.id,
            'layout': {},
            'paint': {
                'line-color': '#000',
                'line-width': this.width
            }
        });
    }
}

function dbscan_polygon() {
    url = "http://localhost:8000/api/geojson/polygon/dbscan"
    id = "dbscan_polygon"
    let dbscan_polygon = new DrawPolygon(url, id, "None", "black", 3, 0.5)
    dbscan_polygon.add_structure();
}
function optics_polygon(eps = 1.0) {
    url = "http://localhost:8000/api/geojson/polygon/optics/" + eps.toFixed(4)
    id = "optics_polygon"
    let optics_polygon = new DrawPolygon(url, id, "None", "black", 3, 0.5);
    optics_polygon.add_structure();
}
//

class ClusteringParam {
    constructor() {
        this.assrp = true
        this.aswp = false
        this.pvsrp = true
        this.pvloc = true
        this.route = false
        this.optics = true
        this.eps = 0.1
        this.printall = true
    }
}

window.onload = function (){
    // create dat.GUI instance
    const gui = new dat.GUI();

    // create parameter instance
    const clustering_param = new ClusteringParam();

    // add parameter object to dat.GUI instance
    gui.add(clustering_param, 'assrp').onChange(function (bool) {
        clustering_param.assrp = bool;
        visible_control(bool, "AsSrp");
    });
    gui.add(clustering_param, 'aswp').onChange(function (bool) {
        clustering_param.aswp = bool;
        visible_control(bool, "AsWp");
    });
    gui.add(clustering_param, 'pvsrp').onChange(function (bool) {
        clustering_param.pvsrp = bool;
        visible_control(bool, "PvSrp");
    });
    gui.add(clustering_param, 'pvloc').onChange(function (bool) {
        clustering_param.pvloc = bool;
        visible_control(bool, "PvLoc");
    });
    gui.add(clustering_param, 'route').onChange(function (bool) {
        clustering_param.route = bool;
        visible_control(bool, "route")
    })
    gui.add(clustering_param, 'optics').onChange(function (bool) {
        clustering_param.optics = bool;
        visible_control(bool, "optics_polygonoutline");
    });
    gui.add(clustering_param, 'eps').name("eps[km]").onChange(function (eps) {
        clustering_param.eps = eps
        set_eps(eps);
    });
    gui.add(clustering_param, 'printall').onChange(function (bool) {
        if (bool) {
            console.log(clustering_param);
        };
    });
    function visible_control(bool, id){
        if (bool) {
            map.setLayoutProperty(id, 'visibility', 'visible');
        }else {
            map.setLayoutProperty(id, 'visibility', 'none');
        }
    }
    function set_eps(eps){
        // TODO
        map.removeLayer("optics_polygonoutline")
        map.removeSource("optics_polygon")
        optics_polygon(eps)
    }
}

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: centers["chofu"], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: init_zoom, // 初期に表示する地図のズームレベル
});

map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());
//map.addControl(new mapboxgl.ScaleControl());
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 200,
    unit: 'metric'
}));

map.on('load', function () {

    //add_routepath();
    asWpPoint();
    asSrpPoint();
    pvSrpPoint();
    pvLocationPoint();
    optics_polygon(0.1);
    //dbscanPoint();
    //dbscan_polygon();
    corner = [[139.53727523803707, 35.6487230630116], [139.55272476196285, 35.66127644371278]]
    addManyMarkers(map, corner)
});