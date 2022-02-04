// Map.js

console.log("map neko");

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';
let centers = { "chofu": [139.545, 35.655], "shibuya": [139.65, 35.65], "maebashi": [139.075, 36.376]};
let init_zoom = [14, 8, 7, 5];

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/kwatanabe1998/ckwvzytdk7ixc14o53kanjxs8',
    center: centers["maebashi"], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: 6, // 初期に表示する地図のズームレベル
    scrollZoom: false
});

map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());
//map.addControl(new mapboxgl.ScaleControl());
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 200,
    unit: 'metric'
}));

function get_window_size() {
    let element = document.getElementById("map")
    return [element.clientWidth, element.clientHeight]
}

function map_unproject() {
    return [get_left_bottom(), get_right_top()]
}

function get_left_bottom() {
    let height = map.getContainer().offsetHeight;
    let p0 = map.unproject([0, height]);

    return [p0["lng"], p0["lat"]]
}
function get_right_top() {
    let width = map.getContainer().offsetWidth;
    let p1 = map.unproject([width, 0]);

    return [p1["lng"], p1["lat"]]
}




export {map, get_window_size, get_left_bottom, get_right_top, map_unproject};