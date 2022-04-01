// GLH.js

import { getReachability, updateReachability } from "./OPTICSdata.js"
import { mapboxmap } from "./Map.js"
import { GUIObject } from "./gui.js";

const map = mapboxmap.map;

function addStructure(){
    ;
};

function initMessage(){
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", map.getZoom());
    console.log("window size:", mapboxmap.unproject());
};

var gui_object;

window.onload = function () {
    let gui = new dat.GUI();
    gui_object = new GUIObject(gui);
}

map.on('load', function () {
    initMessage();
    addStructure();
    getReachability();
});

map.on('moveend', e => {
    console.log('moveend', map.getBounds().toArray());
    updateReachability(gui_object.parameter.eps);
});