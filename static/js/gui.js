import { mapboxmap } from "./Map.js"
import { drawClusters, update_reachability } from "./OPTICSdata.js";

const map = mapboxmap.map;

class GUIParameter {
    constructor() {
        this.points = true
        this.pvloc = false
        this.optics = true
        this.plot = true
        this.eps = 50
        this.printall = true
    }
}

class GUIObject {
    constructor(gui) {
        this.gui = gui;

        this.parameter = new GUIParameter();
        this.add_gui(this.gui, this.parameter)
    }

    getPvloc(){
        return this.convert_visibility(this.parameter.pvloc);
    }
    convert_visibility(bool) {
        return (bool ? "visible" : "none");
    }

    add_gui(gui, parameters) {
        // add parameter object to dat.GUI instance
        gui.add(parameters, 'points').onChange(function (bool) {
            parameters.assrp = bool;
            visible_control(bool, "GLHpoints")
        });

        gui.add(parameters, 'pvloc').onChange(function (bool) {
            parameters.pvloc = bool;
            visible_control(bool, "PvLoc");
        });

        gui.add(parameters, 'optics').onChange(function (bool) {
            parameters.optics = bool;
            visible_control(bool, "clusters_outline");
        });
        gui.add(parameters, 'plot').onChange(function (bool) {
            display_control(bool, "d3plot");
        });

        gui.add(parameters, 'eps').name("eps[km]").onChange(function (eps) {
            parameters.eps = eps;
            set_eps(eps);
        });
        gui.add(parameters, 'printall').onChange(function (bool) {
            if (bool) {
                console.log(parameters);
            };
        });
        display_control(parameters.plot, 'd3plot');
        display_control(parameters.legend, 'state-legend');

        function convert_visibility(bool) {
            return (bool ? "visible" : "none");
        }

        function visible_control(bool, id) {
            map.setLayoutProperty(id, 'visibility', convert_visibility(bool))
        }

        function display_control(bool, id) {
            if (bool) {
                document.getElementById(id).style.display = "block"
            } else {
                document.getElementById(id).style.display = "none"
            }
        }

        function set_eps(eps) {
            mapboxmap.removeOPTICSLayer();
            drawClusters(eps);
            update_reachability(eps);
        }
    };


    set_eps(eps) {
        mapboxmap.removeOPTICSLayer();
        drawClusters(eps);
        update_reachability(eps);
    }
}

export { GUIObject };