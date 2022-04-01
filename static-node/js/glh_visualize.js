import { MapboxMap } from "./modules/Map.js"
import { add_routepath, asSrpPoint, asWpPoint, pvLocationPoint, pvSrpPoint } from "./routing.js";

class GUIParameter {
    constructor() {
        this.as_srp = true
        this.as_wp = true
        this.pv_srp = true
        this.pv_loc = true
    }
}

class GUICotroller {
    constructor() {
        this.parameters = new GUIParameter();
    }

    addGUI(gui) {
        gui.add(this.parameters, 'as_srp').onChange((bool) =>{
            this.parameters.as_srp = bool;
            mapboxmap.layerVisibility('AsSrp', bool);
        });
        gui.add(this.parameters, 'as_wp').onChange((bool) => {
            this.parameters.as_wp = bool;
            mapboxmap.layerVisibility('AsWp', bool);
        });
        gui.add(this.parameters, 'pv_srp').onChange((bool) => {
            this.parameters.pv_srp = bool;
            mapboxmap.layerVisibility('PvSrp', bool);
        });
        gui.add(this.parameters, 'pv_loc').onChange((bool) => {
            this.parameters.pv_loc = bool;
            mapboxmap.layerVisibility('PvLoc', bool);
        });
    }
}

let gui_controller = new GUICotroller();

window.onload = () => {
    let gui = new dat.GUI();
    gui_controller.addGUI(gui);
}

const mapboxmap = new MapboxMap();

mapboxmap.map.on('load', () => {
    //add_routepath(mapboxmap.map, 'gray');
    asSrpPoint(mapboxmap.map, 'blue');
    asWpPoint(mapboxmap.map, 'pink');
    pvSrpPoint(mapboxmap.map, 'yellow');
    pvLocationPoint(mapboxmap.map, 'white');
});


