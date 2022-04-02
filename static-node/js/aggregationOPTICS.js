import { MapboxMap } from "./modules/Map.js";
import { pvLocationPoint } from "./routing.js";
import { getReachability, updateReachability } from "./modules/OPTICSdata.js"

const mapboxmap = new MapboxMap();

class GUIParameter {
    constructor() {
        this.points = true
        this.pv_loc = true
        this.optics = true
        this.eps = 50
    }
}

class GUICotroller {
    constructor() {
        this.parameters = new GUIParameter();
    }

    addGUI(gui) {
        gui.add(this.parameters, 'points').onChange((bool) => {
            this.parameters.points = bool;
            mapboxmap.layerVisibility('Points', bool);
        });
        gui.add(this.parameters, 'pv_loc').onChange((bool) => {
            this.parameters.pv_loc = bool;
            mapboxmap.layerVisibility('PvLoc', bool);
        });
        gui.add(this.parameters, 'optics').onChange((bool) => {
            this.parameters.optics = bool;
            mapboxmap.layerVisibility('clusters_outline', bool);
        });
        gui.add(this.parameters, 'eps').name("eps[km]").onChange((eps) => {
            this.parameters.eps = eps;
            updateReachability(eps);
        })
    }
}

let gui_controller = new GUICotroller();

window.onload = () => {
    let gui = new dat.GUI();
    gui_controller.addGUI(gui);
}



mapboxmap.map.on('load', function () {
    pvLocationPoint(mapboxmap.map, 'white');
    getReachability(mapboxmap);
});

mapboxmap.map.on('moveend', (e) => {
    console.log("moveend", mapboxmap.unproject());
    updateReachability(gui_controller.parameters.eps);
});
