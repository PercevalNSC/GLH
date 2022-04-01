// GLH.js

import {get_reachability, update_reachability} from "./OPTICSdata.js"
import { mapboxmap } from "./Map.js"
import { GUIObject } from "./gui.js";
import { pvLocationPoint } from "./Structure.js";

const map = mapboxmap.map;



function init_message(){
    console.log("map load")
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", map.getZoom());
    console.log("window size:", mapboxmap.map_unproject());
};

var gui_object;

function add_structure(){
    pvLocationPoint(map, "white", gui_object.getPvloc());
};

window.onload = function () {
    console.log("window load")

    let gui = new dat.GUI();
    gui_object = new GUIObject(gui);

    add_structure();
}

map.on('load', function () {
    init_message();
    get_reachability();
});

map.on('moveend', e => {
    console.log('moveend', map.getBounds().toArray());
    update_reachability(gui_object.parameter.eps);
});