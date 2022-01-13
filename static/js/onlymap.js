// GLH.js

neko = 0
//

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
function convert_visibility(bool) {
    if (bool) {
        return "visible"
    } else {
        return "none"
    }
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
    optics_polygon(eps)
}

function get_window_size() {
    element = document.getElementById("map")
    return [element.clientWidth, element.clientHeight]
}
function map_unproject(map) {
    return [get_left_bottom(map), get_right_top(map)]
}
function get_left_bottom(map) {
    let height = map.getContainer().offsetHeight;
    let p0 = map.unproject([0, height]);

    return [p0["lng"], p0["lat"]]
}
function get_right_top(map) {
    let width = map.getContainer().offsetWidth;
    let p1 = map.unproject([width, 0]);

    return [p1["lng"], p1["lat"]]
}

mapboxgl.accessToken = 'pk.eyJ1Ijoia3dhdGFuYWJlMTk5OCIsImEiOiJja29tNnQyNnIwZXZxMnVxdHQ1aXllMGRiIn0.ebm4ShyOk1Mp-W1xs0G_Ag';
centers = { "chofu": [139.545, 35.655], "shibuya": [139.65, 35.65], "maebashi": [139.075, 36.376]};
init_zoom = 14;

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/kwatanabe1998/ckwvzytdk7ixc14o53kanjxs8',
    center: centers["maebashi"], // 初期に表示する地図の緯度経度 [経度、緯度]（緯度、経度とは順番が異なりますのでご注意下さい）
    zoom: init_zoom, // 初期に表示する地図のズームレベル
    scrollZoom: false
});

map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());
//map.addControl(new mapboxgl.ScaleControl());
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 200,
    unit: 'metric'
}));

const clustering_param = new ClusteringParam();

map.on('load', function () {
    console.log("map load")
    console.log("map center:", map.getCenter());
    console.log("init zoom level:", init_zoom);
    console.log("window size:", get_window_size());
    add_routepath("white", convert_visibility(clustering_param.route));
    asWpPoint("white", convert_visibility(clustering_param.aswp));
    asSrpPoint("pink", convert_visibility(clustering_param.assrp));
    pvSrpPoint("pink", convert_visibility(clustering_param.pvsrp));
    pvLocationPoint("white", convert_visibility(clustering_param.pvloc));
    optics_polygon(0.1);

});

window.onload = function () {
    console.log("window load")
    // create dat.GUI instance
    const gui = new dat.GUI();

    // create parameter instance

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
    display_control(clustering_param.legend, 'state-legend');
}