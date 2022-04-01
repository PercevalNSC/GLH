import { mapboxmap } from "./Map.js"
import { drawClusters, updateReachability } from "./OPTICSdata.js";

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
        this.addGui(this.gui, this.parameter)
    }

    convertVisibility(bool) {
        return (bool ? "visible" : "none");
    }

    addGui(gui, parameters) {
        // add parameter object to dat.GUI instance
        gui.add(parameters, 'points').onChange(function (bool) {
            parameters.assrp = bool;
            visibleControl(bool, "GLHpoints")
        });

        gui.add(parameters, 'pvloc').onChange(function (bool) {
            parameters.pvloc = bool;
            visibleControl(bool, "PvLoc");
        });

        gui.add(parameters, 'optics').onChange(function (bool) {
            parameters.optics = bool;
            visibleControl(bool, "clusters_outline");
        });
        gui.add(parameters, 'plot').onChange(function (bool) {
            displayControl(bool, "d3plot");
        });

        gui.add(parameters, 'eps').name("eps[km]").onChange(function (eps) {
            parameters.eps = eps;
            setEps(eps);
        });
        gui.add(parameters, 'printall').onChange(function (bool) {
            if (bool) {
                console.log(parameters);
            };
        });
        displayControl(parameters.plot, 'd3plot');
        displayControl(parameters.legend, 'state-legend');

        function convertVisibility(bool) {
            return (bool ? "visible" : "none");
        }

        function visibleControl(bool, id) {
            map.setLayoutProperty(id, 'visibility', convertVisibility(bool))
        }

        function displayControl(bool, id) {
            if (bool) {
                document.getElementById(id).style.display = "block"
            } else {
                document.getElementById(id).style.display = "none"
            }
        }

        function setEps(eps) {
            mapboxmap.removeOPTICSLayer();
            drawClusters(eps);
            update_reachability(eps);
        }
    };


    setEps(eps) {
        mapboxmap.removeOPTICSLayer();
        drawClusters(eps);
        updateReachability(eps);
    }
}

export { GUIObject };