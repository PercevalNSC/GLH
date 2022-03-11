// GLH.js

import { get_reachability, update_reachability } from "./OPTICSdata.js"
import { mapboxmap } from "./Map.js"
import { GUIObject } from "./gui.js";

const map = mapboxmap.map;

function add_structure(){
    ;
};

function init_message(){
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", map.getZoom());
    console.log("window size:", mapboxmap.map_unproject());
};

var gui_object;

window.onload = function () {
    let gui = new dat.GUI();
    gui_object = new GUIObject(gui);
}

map.on('load', function () {
    init_message();
    add_structure();
    get_reachability();
});

map.on('moveend', e => {
    console.log('moveend', map.getBounds().toArray());
    update_reachability(gui_object.parameter.eps);
});