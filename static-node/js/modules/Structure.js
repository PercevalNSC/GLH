// Stricture.js

class GeoJsonStructure {
    constructor(map, id, color, opacity, visibility) {
        this.map = map;
        this.id = id;
        this.color = color;
        this.opacity = opacity;
        this.visibility = visibility;
    }
    addStructure(geojson) {
        this.geojson = geojson;
        this._addGeojson()
    }
    _addGeojson() {
        this._addSource();
        this._addLayer();
    }
    _addSource() {
        this.map.addSource(this.id, {
            'type': 'geojson',
            'data': this.geojson
        });
    }
    _addLayer() {
        // specified structure
        this.map.addLayer({
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

class GeojsonPointStructure extends GeoJsonStructure {
    constructor(map, id, color = "black", opacity = 1.0, visibility = "visible", radius = 4) {
        super(map, id, color, opacity, visibility);
        this.radius = radius;
    }
    _addLayer() {
        this.map.addLayer({
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
        this._clickPopup();
    }
    _clickPopup() {
        this.map.on('click', this.id, function (e) {
            var coordinates = e.features[0].geometry.coordinates.slice();
            var date = new Date(e.features[0].properties.timestamp)
            var description = "Timestamp:" + date.toString();
            new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(this.map);
        });
    }
}

class GeoJsonLineStructure extends GeoJsonStructure {
    constructor(map, id, color = "black", opacity = 0.5, visibility = "visible", width = 1) {
        super(map, id, color, opacity, visibility);
        this.width = width;
        console.log("width:", this.width);
    }
    _addLayer() {
        this.map.addLayer({
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
                'line-width': this.width,
            }
        });
    }
}

class GeoJsonPolygonStructure extends GeoJsonStructure {
    constructor(map, id, color = "white", opacity = 0.5, visibility = "visible", width = 3, linecolor = "black") {
        super(map, id, color, opacity, visibility);
        this.width = width;
        this.linecolor = linecolor;
    }
    _addLayer() {
        if (this.color != "None") {
            this._addFillLayer();
        };
        this._addSurroundLayer();
    }
    _addFillLayer() {
        this.map.addLayer({
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
    _addSurroundLayer() {
        this.map.addLayer({
            'id': this.id + "_outline",
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


class DrawPoints extends GeojsonPointStructure {
    constructor(map, url, id, color = 'black', radius = 4, opacity = 1.0, visibility) {
        super(map, id, color, opacity, visibility, radius);
        this.url = url;
    }
    addStructure() {
        fetch(this.url, {
            mode: 'cors'
        }).then((response) => {
            return response.json();
        }).then((geojson) => {
            this.geojson = geojson;
            this._addGeojson();
            console.log("Write: " + this.url);
        }).catch((e) => {
            console.log(e);
        });
    }
}

class DrawLine extends GeoJsonLineStructure {
    constructor(map, url, id, color = 'black', width = 1, opacity = 0.5, visibility = 'visible') {
        super(map, id, color, opacity, visibility, width);
        this.url = url;
    }
    addStructure() {
        fetch(this.url, {
            mode: 'cors'
        }).then((response) => {
            return response.json();
        }).then((geojson) => {
            this.geojson = geojson;
            this._addGeojson();
            console.log("Write: " + this.url);
        }).catch((e) => {
            console.log(e);
        });
    }
}
class DrawPolygon extends GeoJsonPolygonStructure {
    constructor(map, url, id, fillcolor = "white", linecolor = "black", width = 3, opacity = 0.5, visibility = "visivle") {
        super(map, id, fillcolor, opacity, visibility, width, linecolor);
        this.url = url;
    }
    addStructure() {
        fetch(this.url, {
            mode: 'cors'
        }).then((response) => {
            return response.json();
        }).then((geojson) => {
            this.geojson = geojson;
            this._addGeojson();
            console.log("Write: " + this.url);
        }).catch((e) => {
            console.log(e);
        });
    }
}

function asSrpPoint(map, color = "blue", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/activitySegment.simplifiedRawPath"
    let as_srp_point = new DrawPoints(map, url, "AsSrp");
    as_srp_point.color = color
    as_srp_point.visibility = visibility
    as_srp_point.addStructure();
}
function asWpPoint(map, color = "pink", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/activitySegment.waypointPath"
    let as_wp_point = new DrawPoints(map, url, "AsWp");
    as_wp_point.color = color;
    as_wp_point.visibility = visibility;
    as_wp_point.addStructure();
}
function pvSrpPoint(map, color = "yellow", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/placeVisit.simplifiedRawPath"
    let pv_srp_point = new DrawPoints(map, url, "PvSrp");
    pv_srp_point.color = color;
    pv_srp_point.visibility = visibility;
    pv_srp_point.addStructure();
}
function pvLocationPoint(map, color = "white", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/placeVisit.location"
    let pv_location = new DrawPoints(map, url, "PvLoc", color, 6, 1, visibility);
    pv_location.addStructure();
}
function dbscan_point(map, color = "red", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/dbscan"
    let dbscan_point = new DrawPoints(map, url, "dbscan_point");
    dbscan_point.color = color;
    dbscan_point.visibility = visibility;
    dbscan_point.addStructure();
}

function add_routepath(map, color = 'gray', visibility = "visible", opacity = 0.5, width = 1) {
    let url = "http://localhost:8000/api/geojson/line/route"
    let id = "routepath"
    let routepath = new DrawLine(map, url, id, color, width, opacity, visibility);
    routepath.addStructure();
}



function dbscan_polygon(map, fillcolor = "None", linecolor = "black") {
    let url = "http://localhost:8000/api/geojson/polygon/dbscan"
    let id = "dbscan_polygon"
    let dbscan_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 3, 0.5)
    dbscan_polygon.addStructure();
}
function optics_polygon(map, eps = 1.0, fillcolor = "None", linecolor = "black") {
    let url = "http://localhost:8000/api/geojson/polygon/optics/" + eps.toFixed(10)
    let id = "optics_polygon"
    let optics_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 3, 0.6);
    optics_polygon.addStructure();
}
function viewport_polygon(map, fillcolor = "None", linecolor = "gray") {
    let url = "http://localhost:8000/api/geojson/viewport";
    let id = "viewport";
    let viewport_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 2, 0.3);
    viewport_polygon.addStructure();
}

export {GeojsonPointStructure, GeoJsonLineStructure, GeoJsonPolygonStructure, asSrpPoint, asWpPoint, pvSrpPoint, pvLocationPoint, dbscan_point, add_routepath, dbscan_polygon, optics_polygon, viewport_polygon};
