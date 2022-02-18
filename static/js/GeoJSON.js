class GeoJson {
    constructor(name, list) {
        this.geojson = {
            "type": "FeatureCollection",
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": this.makingFeatures(list)
        }
    }

    makingFeatures(list) {
        console.log("Undefined geojson class.");
        return list;
    }
}

class PointGeoJson extends GeoJson {
    constructor(name, points) {
        super(name, points);
    }

    makingFeatures(points) {
        let features = [];
        points.forEach(p => {
            let feature = {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Point",
                    "coordinates": p
                }
            }
            features.push(feature);
        });
        return features;
    }
}

class LineGeoJson {
    constructor(name, points) {
        this.geojson = {
            "type": "LineString",
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "coordinates": points
        }
    }
}

class PolygonGeoJson{
    constructor(name, polygons) {
        this.geojson = {
            'type': 'Feature',
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': polygons
            }
        };
    }
}

export {PointGeoJson, LineGeoJson, PolygonGeoJson}