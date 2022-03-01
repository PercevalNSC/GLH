// Map.js

import { GeojsonPointStructure, GeoJsonLineStructure, GeoJsonPolygonStructure } from "./Structure.js"

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';
let centers = { "chofu": [139.545, 35.655], "shibuya": [139.65, 35.65], "maebashi": [139.075, 36.376] };
let init_zoom = [14, 8, 7, 5];

class MapboxMap {
    constructor() {
        console.log("map load")
        this.map = this.#addMap();
        this.#addControl();
    }

    map_unproject() {
        // 左下と右上の座標のリスト
        return [this.get_left_bottom(), this.get_right_top()]
    }

    get_left_bottom() {
        let height = this.map.getContainer().offsetHeight;
        let p = this.map.unproject([0, height]);

        return [p["lng"], p["lat"]]
    }
    get_right_top() {
        let width = this.map.getContainer().offsetWidth;
        let p = this.map.unproject([width, 0]);

        return [p["lng"], p["lat"]]
    }
    removeOPTICSLayer() {
        this.map.removeLayer("clusters_outline");
        this.map.removeSource("clusters");
    }
    addGeojsonPoints(geojson, id) {
        let geojson_points = new GeojsonPointStructure(this.map, id);
        geojson_points.add_structure(geojson);
    }
    addGeojsonLine(geojson, id) {
        let geojson_line = new GeoJsonLineStructure(this.map, id);
        geojson_line.add_structure(geojson);
    }
    addGeojonPolygons(geojson, id) {
        let geojson_polygons = new GeoJsonPolygonStructure(this.map, id, "None");
        geojson_polygons.add_structure(geojson);
    }

    #addMap() {
        return new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/kwatanabe1998/ckwvzytdk7ixc14o53kanjxs8',
            center: centers["maebashi"], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
            zoom: 6, // 初期に表示する地図のズームレベル
            scrollZoom: false
        });
    }
    #addControl() {
        this.map.addControl(new mapboxgl.FullscreenControl());
        this.map.addControl(new mapboxgl.NavigationControl());
        //map.addControl(new mapboxgl.ScaleControl());
        this.map.addControl(new mapboxgl.ScaleControl({
            maxWidth: 200,
            unit: 'metric'
        }));
    }
}

const mapboxmap = new MapboxMap();

export { mapboxmap };