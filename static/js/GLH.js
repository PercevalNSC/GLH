// GLH.js

import * as Structure from "./Structure.js"
import {get_reachability} from "./d3plot.js"
import {map, get_window_size} from "./Map.js"

class ClusteringParam {
    constructor() {
        this.assrp = true
        this.aswp = false
        this.pvsrp = true
        this.pvloc = false
        this.route = false
        this.optics = true
        this.plot = true
        this.legend = false
        this.eps = 0.1
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
    // TODO
    map.removeLayer("optics_polygonoutline")
    map.removeSource("optics_polygon")
    Structure.optics_polygon(map, eps)
}



function init_message(){
    console.log("map load")
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", map.getZoom());
    console.log("window size:", get_window_size());
};
function add_structure(){
    Structure.add_routepath(map, "white", convert_visibility(clustering_param.route));
    Structure.asWpPoint(map, "white", convert_visibility(clustering_param.aswp));
    Structure.asSrpPoint(map, "pink", convert_visibility(clustering_param.assrp));
    Structure.pvSrpPoint(map, "pink", convert_visibility(clustering_param.pvsrp));
    Structure.pvLocationPoint(map, "white", convert_visibility(clustering_param.pvloc));
    Structure.optics_polygon(map, 0.1);
};

function add_gui(gui, clustering_param){
    // add parameter object to dat.GUI instance
    gui.add(clustering_param, 'assrp').onChange(function (bool) {
        clustering_param.assrp = bool;
        visible_control(bool, "AsSrp");
    });
    gui.add(clustering_param, 'aswp').onChange(function (bool) {
        clustering_param.aswp = bool;
        visible_control(bool, "AsWp");
    });
    gui.add(clustering_param, 'pvsrp').onChange(function (bool) {
        clustering_param.pvsrp = bool;
        visible_control(bool, "PvSrp");
    });
    gui.add(clustering_param, 'pvloc').onChange(function (bool) {
        clustering_param.pvloc = bool;
        visible_control(bool, "PvLoc");
    });
    gui.add(clustering_param, 'route').onChange(function (bool) {
        clustering_param.route = bool;
        visible_control(bool, "routepath")
    })
    gui.add(clustering_param, 'optics').onChange(function (bool) {
        clustering_param.optics = bool;
        visible_control(bool, "optics_polygonoutline");
    });
    gui.add(clustering_param, 'plot').onChange(function (bool) {
        display_control(bool, "d3plot");
    });
    gui.add(clustering_param, 'legend').onChange(function (bool) {
        display_control(bool, "state-legend");
    })
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


window.onload = function () {
    console.log("window load")
    // create dat.GUI instance
    const gui = new dat.GUI();

    // create parameter instance

    add_gui(gui, clustering_param)
}