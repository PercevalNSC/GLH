import { MapboxMap } from "./modules/Map.js"
import { add_routepath, asSrpPoint, asWpPoint, pvLocationPoint, pvSrpPoint } from "./routing.js";

const mapboxmap = new MapboxMap();

mapboxmap.map.on('load', () => {
    //add_routepath(mapboxmap.map, 'gray');
    asSrpPoint(mapboxmap.map, 'blue');
    asWpPoint(mapboxmap.map, 'pink');
    pvSrpPoint(mapboxmap.map, 'yellow');
    pvLocationPoint(mapboxmap.map, 'white');
});

