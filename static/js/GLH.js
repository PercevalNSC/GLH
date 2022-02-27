// GLH.js

import { get_reachability, update_reachability, drawClusters} from "./OPTICSdata.js"
import { map, get_window_size} from "./Map.js"
import { pvLocationPoint } from "./Structure.js"

class ClusteringParam {
    constructor() {
        this.points = true
        this.pvloc = false
        this.optics = true
        this.plot = true
        this.eps = 10
        this.printall = true
    }
}

const clustering_param = new ClusteringParam();

function convert_visibility(bool) {
    return (bool ? "visible" : "none");
}
function display_control(bool, id) {
    if (bool) {
        document.getElementById(id).style.display = "block"
    } else {
        document.getElementById(id).style.display = "none"
    }
}
function visible_control(bool, id) {
    map.setLayoutProperty(id, 'visibility', convert_visibility(bool))
}
function set_eps(eps) {
    update_optics_layer(eps);
    update_reachability(map, eps);
}
function update_optics_layer(eps) {
    map.removeLayer("clustersoutline");
    map.removeSource("clusters");
    drawClusters(map, eps);
}

function init_message(){
    console.log("map load")
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", map.getZoom());
    console.log("window size:", get_window_size());
};
function add_structure(){
    pvLocationPoint(map, "white", convert_visibility(clustering_param.pvloc))
};

function add_gui(gui, clustering_param){
    // add parameter object to dat.GUI instance
    gui.add(clustering_param, 'points').onChange(function (bool) {
        clustering_param.assrp = bool;
        visible_control(bool, "GLHpoints");
    });

    gui.add(clustering_param, 'pvloc').onChange(function (bool) {
        clustering_param.pvloc = bool;
        visible_control(bool, "PvLoc");
    });

    gui.add(clustering_param, 'optics').onChange(function (bool) {
        clustering_param.optics = bool;
        visible_control(bool, "clusterssoutline");
    });
    gui.add(clustering_param, 'plot').onChange(function (bool) {
        display_control(bool, "d3plot");
    });

    gui.add(clustering_param, 'eps').name("eps[km]").onChange(function (eps) {
        clustering_param.eps = eps
        set_eps(eps);
    });
    gui.add(clustering_param, 'printall').onChange(function (bool) {
        if (bool) {
            console.log(clustering_param);
        };
    });
    display_control(clustering_param.plot, 'd3plot');
    display_control(clustering_param.legend, 'state-legend');
};

map.on('load', function () {
    init_message();
    add_structure();
    get_reachability(map);
});
map.on('moveend', e => {
    console.log('moveend', map.getBounds().toArray());
    update_reachability(map, clustering_param.eps);
});

window.onload = function () {
    console.log("window load")
    // create dat.GUI instance
    const gui = new dat.GUI();

    // create parameter instance

    add_gui(gui, clustering_param)
}