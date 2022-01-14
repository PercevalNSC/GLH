// Stricture.js

console.log("structure neko");


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
    constructor(map, url, id, color, opacity, visibility) {
        this.map = map;
        this.url = url;
        this.id = id;
        this.color = color;
        this.opacity = opacity;
        this.visibility = visibility;
    }
    add_structure() {
        fetch(this.url, {
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
        this.map.addSource(this.id, {
            'type': 'geojson',
            'data': geojson
        });
    }
    _add_layer() {
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

class DrawPoints extends DrawStructure {
    constructor(map, url, id, color = 'black', radius = 4, opacity = 1.0, visibility = 'visible') {
        super(map, url, id, color, opacity, visibility);
        this.radius = radius
    }
    _add_layer() {
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
        this._click_popup();
    }
    _click_popup() {
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
function asSrpPoint(map, color = "blue", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/activitySegment.simplifiedRawPath"
    let as_srp_point = new DrawPoints(map, url, "AsSrp");
    as_srp_point.color = color
    as_srp_point.visibility = visibility
    as_srp_point.add_structure();
}
function asWpPoint(map, color = "pink", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/activitySegment.waypointPath"
    let as_wp_point = new DrawPoints(map, url, "AsWp");
    as_wp_point.color = color;
    as_wp_point.visibility = visibility;
    as_wp_point.add_structure();
}
function pvSrpPoint(map, color = "yellow", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/placeVisit.simplifiedRawPath"
    let pv_srp_point = new DrawPoints(map, url, "PvSrp");
    pv_srp_point.color = color;
    pv_srp_point.visibility = visibility;
    pv_srp_point.add_structure();
}
function pvLocationPoint(map, color = "white", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/placeVisit.location"
    let pv_location = new DrawPoints(map, url, "PvLoc", color, 6, 1, visibility);
    pv_location.add_structure();
}
function dbscan_point(map, color = "red", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/dbscan"
    let dbscan_point = new DrawPoints(map, url, "dbscan_point");
    dbscan_point.color = color;
    dbscan_point.visibility = visibility;
    dbscan_point.add_structure();
}
class DrawLine extends DrawStructure {
    constructor(map, url, id, color = 'black', width = 1, opacity = 0.5, visibility = 'visible') {
        super(map, url, id, color, opacity, visibility);
        this.witdh = width
    }
    _add_layer() {
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
                'line-width': this.witdh
            }
        });
    }
}

function add_routepath(map, color = 'gray', visibility = "visible", opacity = 0.5, width = 1) {
    let url = "http://localhost:8000/api/geojson/line/route"
    let id = "routepath"
    let routepath = new DrawLine(map, url, id, color, width, opacity, visibility);
    routepath.add_structure();
}

class DrawPolygon extends DrawStructure {
    constructor(map, url, id, fillcolor = "white", linecolor = "black", width = 3, opacity = 0.5, visibility = "visivle") {
        super(map, url, id, fillcolor, opacity, visibility);
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
    _add_surround_layer() {
        this.map.addLayer({
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

function dbscan_polygon(map, fillcolor = "None", linecolor = "black") {
    let url = "http://localhost:8000/api/geojson/polygon/dbscan"
    let id = "dbscan_polygon"
    let dbscan_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 3, 0.5)
    dbscan_polygon.add_structure();
}
function optics_polygon(map, eps = 1.0, fillcolor = "None", linecolor = "black") {
    let url = "http://localhost:8000/api/geojson/polygon/optics/" + eps.toFixed(10)
    let id = "optics_polygon"
    let optics_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 3, 0.6);
    optics_polygon.add_structure();
}
function viewport_polygon(map, fillcolor = "None", linecolor = "gray") {
    let url = "http://localhost:8000/api/geojson/viewport";
    let id = "viewport";
    let viewport_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 2, 0.3);
    viewport_polygon.add_structure();
}

export {asSrpPoint, asWpPoint, pvSrpPoint, pvLocationPoint, dbscan_point, add_routepath, dbscan_polygon, optics_polygon, viewport_polygon};
