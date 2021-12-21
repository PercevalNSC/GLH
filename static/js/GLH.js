// GLH.js

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
    constructor(url, id, color, opacity, visibility) {
        this.url = url;
        this.id = id;
        this.color = color;
        this.opacity = opacity;
        this.visibility = visibility;
    }
    add_structure() {
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
    _add_geojson(geojson) {
        this._add_source(geojson);
        this._add_layer();

    }
    _add_source(geojson) {
        map.addSource(this.id, {
            'type': 'geojson',
            'data': geojson
        });
    }
    _add_layer() {
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

class DrawPoints extends DrawStructure {
    constructor(url, id, color = 'black', radius = 4, opacity = 1.0, visibility = 'visible') {
        super(url, id, color, opacity, visibility);
        this.radius = radius
    }
    _add_layer() {
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
    _click_popup() {
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
function asSrpPoint(color = "blue", visibility = "visible") {
    url = "http://localhost:8000/api/geojson/point/activitySegment.simplifiedRawPath"
    let as_srp_point = new DrawPoints(url, "AsSrp");
    as_srp_point.color = color
    as_srp_point.visibility = visibility
    as_srp_point.add_structure();
}
function asWpPoint(color = "pink", visibility = "visible") {
    url = "http://localhost:8000/api/geojson/point/activitySegment.waypointPath"
    let as_wp_point = new DrawPoints(url, "AsWp");
    as_wp_point.color = color;
    as_wp_point.visibility = visibility;
    as_wp_point.add_structure();
}
function pvSrpPoint(color = "yellow", visibility = "visible") {
    url = "http://localhost:8000/api/geojson/point/placeVisit.simplifiedRawPath"
    let pv_srp_point = new DrawPoints(url, "PvSrp");
    pv_srp_point.color = color;
    pv_srp_point.visibility = visibility;
    pv_srp_point.add_structure();
}
function pvLocationPoint(color = "white", visibility = "visible") {
    url = "http://localhost:8000/api/geojson/point/placeVisit.location"
    let pv_location = new DrawPoints(url, "PvLoc", color = color, radius = 6, opacity = 1, visibility = visibility);
    pv_location.add_structure();
}
function dbscan_point(color = "red", visibility = "visible") {
    url = "http://localhost:8000/api/geojson/point/dbscan"
    let dbscan_point = new DrawPoints(url, "dbscan_point");
    dbscan_point.color = color;
    dbscan_point.visibility = visibility;
    dbscan_point.add_structure();
}
class DrawLine extends DrawStructure {
    constructor(url, id, color = 'black', width = 1, opacity = 0.5, visibility = 'visible') {
        super(url, id, color, opacity, visibility);
        this.witdh = width
    }
    _add_layer() {
        map.addLayer({
            'id': this.id,
            'type': 'line',
            'source': this.id,
            'layout': {
                'line-join': 'bevel',
                'line-cap': 'butt',
                'visibility': this.visibility
            },
            'paint': {
                'line-color': this.color,
                'line-opacity': this.opacity,
                'line-width': this.witdh
            }
        });
    }
}

function add_routepath(color = 'gray', visibility = "visible", opacity = 0.5, width = 1) {
    url = "http://localhost:8000/api/geojson/line/route"
    id = "routepath"
    let routepath = new DrawLine(url, id, color, width, opacity, visibility);
    routepath.add_structure();
}

class DrawPolygon extends DrawStructure {
    constructor(url, id, fillcolor = "white", linecolor = "black", width = 3, opacity = 0.5, visibility = "visivle") {
        super(url, id, fillcolor, opacity, visibility);
        this.linecolor = linecolor;
        this.width = width;
    }
    _add_layer() {
        if (this.color != "None") {
            this._add_fill_layer();
        };
        this._add_surround_layer();
    }
    _add_fill_layer() {
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
    _add_surround_layer() {
        map.addLayer({
            'id': this.id + "outline",
            'type': 'line',
            'source': this.id,
            'layout': {},
            'paint': {
                'line-color': this.linecolor,
                'line-width': this.width
            }
        });
    }
}

function dbscan_polygon(fillcolor = "None", linecolor = "black") {
    url = "http://localhost:8000/api/geojson/polygon/dbscan"
    id = "dbscan_polygon"
    let dbscan_polygon = new DrawPolygon(url, id, fillcolor, linecolor, 3, 0.5)
    dbscan_polygon.add_structure();
}
function optics_polygon(eps = 1.0, fillcolor = "None", linecolor = "black") {
    url = "http://localhost:8000/api/geojson/polygon/optics/" + eps.toFixed(10)
    id = "optics_polygon"
    let optics_polygon = new DrawPolygon(url, id, fillcolor, linecolor, 3, 0.6);
    optics_polygon.add_structure();
}
function viewport_polygon(fillcolor = "None", linecolor = "gray") {
    url = "http://localhost:8000/api/geojson/viewport";
    id = "viewport";
    let viewport_polygon = new DrawPolygon(url, id, fillcolor, linecolor, 2, 0.3);
    viewport_polygon.add_structure();
}
//

class ClusteringParam {
    constructor() {
        this.assrp = true
        this.aswp = false
        this.pvsrp = true
        this.pvloc = false
        this.route = false
        this.optics = true
        this.plot = false
        this.legend = false
        this.eps = 0.1
        this.printall = true
    }

}
function convert_visibility(bool) {
    if (bool) {
        return "visible"
    } else {
        return "none"
    }
}


const clustering_param = new ClusteringParam();

window.onload = function () {
    console.log("window load")
    // create dat.GUI instance
    const gui = new dat.GUI();

    // create parameter instance

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
        visible_control(bool, "routepath")
    })
    gui.add(clustering_param, 'optics').onChange(function (bool) {
        clustering_param.optics = bool;
        visible_control(bool, "optics_polygonoutline");
    });
    gui.add(clustering_param, 'plot').onChange(function (bool) {
        display_control(bool, "plot");
    });
    gui.add(clustering_param, 'legend').onChange(function (bool) {
        display_control(bool, "state-legend");
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
    display_control(clustering_param.plot, "plot");
    display_control(clustering_param.legend, "state-legend");

    function display_control(bool, id) {
        if (bool) {
            document.getElementById(id).style.display = "block"
        } else {
            document.getElementById(id).style.display = "none"
        }
    }
    function visible_control(bool, id) {
        map.setLayoutProperty(id, 'visibility', convert_visibility(bool))
    }
    function set_eps(eps) {
        // TODO
        map.removeLayer("optics_polygonoutline")
        map.removeSource("optics_polygon")
        optics_polygon(eps)
    }
}
function get_window_size() {
    return [window.innerWidth, window.innerHeight]
}

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';
centers = { "chofu": [139.545, 35.655], "shibuya": [139.65, 35.65], "Maebashi": [139.075, 36.376]};
init_zoom = 14;

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/kwatanabe1998/ckwvzytdk7ixc14o53kanjxs8',
    center: centers["Maebashi"], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: init_zoom, // 初期に表示する地図のズームレベル
    scrollZoom: false
});

map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());
//map.addControl(new mapboxgl.ScaleControl());
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 200,
    unit: 'metric'
}));

map.on('load', function () {
    console.log("map load")
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", init_zoom);
    console.log("window size:", get_window_size());
    add_routepath("white", convert_visibility(clustering_param.route));
    asWpPoint("white", convert_visibility(clustering_param.aswp));
    asSrpPoint("pink", convert_visibility(clustering_param.assrp));
    pvSrpPoint("pink", convert_visibility(clustering_param.pvsrp));
    pvLocationPoint("white", convert_visibility(clustering_param.pvloc));
    optics_polygon(0.1);
});