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


export {GeojsonPointStructure, GeoJsonLineStructure, GeoJsonPolygonStructure,
    DrawPoints, DrawLine, DrawPolygon};
