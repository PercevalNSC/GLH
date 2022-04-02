// d3plot.js

import { PointGeoJson, PolygonGeoJson } from "./GeoJSON.js"
import { GeojsonPointStructure, GeoJsonPolygonStructure } from "./Structure.js"
import { ReachabilityPlotWithEPS } from "./D3chart.js";

let ID = "d3plot"
let MARGIN = 8
let WIDTH;
let HEIGHT;
let PADDING = 30;

class ReachabilityPlotWithMap extends ReachabilityPlotWithEPS {
    constructor(reachability, width, height, padding) {
        super(reachability, width, height, padding);
    }
    _dragFunction() {
        let yScale = this.yScale;
        var drag_yScale = d3.scaleLinear()
            .clamp(true)    //範囲外を丸める
            .domain([this.padding, this.height - this.padding])
            .range([this.padding, this.height - this.padding]);

        function update_eps() {
            console.log("update eps");
            let eps = yScale.invert(d3.event.y);
            mapboxmap.removeOPTICSLayer();
            drawClusters(eps)
        }

        return d3.drag()
            .on("drag", function () {
                d3.select(this).attr("y", drag_yScale(d3.event.y));
                update_eps();
            })
            .on("end", function () {
                console.log("drag end at:", yScale.invert(d3.event.y))
                update_eps();
            });
    }
}

class OPTICSData {
    constructor(coordinates, reachability, ordering) {
        this.coordinates = coordinates;
        this.reachability = reachability;
        this.ordering = ordering;
    }
    _vieport(mapboxmap) {
        let p0 = mapboxmap.getLeftBottom();
        let p1 = mapboxmap.getRightTop();
        return [p0, p1];
    }
    reachabilityPlot(element_id, eps = 0) {
        let data = this.reachability
        let plot_obj = new ReachabilityPlotWithMap(data, WIDTH, HEIGHT, PADDING);
        plot_obj.plot(element_id, eps);
    };
    aggregateReachability() {
        this.vieport = this._vieport(mapboxmap);
        console.log("map scope by", this.vieport);
        let zoom_coordinates = []
        let zoom_reachability = []
        let zoom_ordering = []
        let out_ordering = []
        let out_max_reachability = 0
        this.coordinates.forEach((coordinate, i) => {
            if (this._isInMap(coordinate)) {
                if (out_max_reachability != 0) {
                    // add virtual point 
                    zoom_coordinates.push([0, 0]);
                    zoom_reachability.push(out_max_reachability);
                    zoom_ordering.push(this.ordering[i - 1]);
                    out_ordering.push(this.ordering[i - 1]);
                };
                // add in map point
                zoom_coordinates.push(coordinate);
                zoom_reachability.push(this.reachability[i]);
                zoom_ordering.push(this.ordering[i]);
                out_max_reachability = 0;
            } else {
                if (this.reachability[i] != "inf") {
                    out_max_reachability = Math.max(out_max_reachability, this.reachability[i]);
                }
                if (i == this.coordinates.length - 1) {
                    zoom_coordinates.push([0, 0]);
                    zoom_reachability.push(out_max_reachability);
                    zoom_ordering.push(this.ordering[i]);
                    out_ordering.push(this.ordering[i]);
                }
            };
        })
        return new ScopedOPTICSData(
            zoom_coordinates, zoom_reachability, zoom_ordering,
            out_ordering);
    };
    _isInMap(coordinate) {
        let p0 = this.vieport[0];
        let p1 = this.vieport[1];
        let x = coordinate[0];
        let y = coordinate[1];
        if (p0[0] <= x && x <= p1[0] && p0[1] <= y && y <= p1[1]) {
            return true;
        } else {
            return false;
        };
    };

    // 降順の極大値のリスト
    reachabilityMaxima(reachability) {
        let boundary_list = []
        let down_index_list = []
        let last = reachability.length - 1
        for (let i = 1; i < last; i++) {
            if (reachability[i] > reachability[i + 1]) {
                down_index_list.push(i);
            };
        };
        for (let down_index of down_index_list) {
            if (reachability[down_index - 1] < reachability[down_index]) {
                boundary_list.push(reachability[down_index]);
            };
        };
        if (reachability[0] >= reachability[1]) {
            boundary_list.push(reachability[0]);
        };
        if (reachability[last - 1] <= reachability[last]) {
            boundary_list.push(reachability[last]);
        };
        return boundary_list;
    }

    outputClusters(eps) {
        let polygons = []
        let cluster_points = []
        this.reachability.forEach((r, i) => {
            if (r <= eps) {
                cluster_points.push(this.coordinates[i]);
                if (i == this.reachability.length - 1) {
                    polygons.push(this._clusterToPolygon(cluster_points));
                };
            } else if (cluster_points.length != 0) {
                polygons.push(this._clusterToPolygon(cluster_points));
                cluster_points = [];
            } else {
                ;
            };
        })
        return polygons.filter(data => data != null);
    }
    _clusterToPolygon(cluster_points) {
        let convexhull = d3.polygonHull(cluster_points);
        return convexhull
    }
    coodinatesToGeojson() {
        let geojsonobj = new PointGeoJson("GLHpoint", this.coordinates);
        return geojsonobj.geojson;
    }
    clustersToGeojson(eps) {
        let geojsonobj = new PolygonGeoJson("Clusters", this.outputClusters(eps));
        console.log(geojsonobj.geojson)
        return geojsonobj.geojson;
    }

    status() {
        console.log("Coordinates:", this.coordinates);
        console.log("Reachability:", this.reachability);
        console.log("Ordering:", this.ordering);
    };
}
class ScopedOPTICSData extends OPTICSData {
    constructor(coordinates, reachability, ordering, out_ordering) {
        super(coordinates, reachability, ordering, mapboxmap);
        this.out_ordering = out_ordering;
    };
    reachabilityPlot(element_id, eps = 0) {
        let data = this.limitOutReachability(this.reachability, this.ordering, this.out_ordering);
        let plot_obj = new ReachabilityPlotWithMap(data, WIDTH, HEIGHT, PADDING);
        plot_obj.plot(element_id, eps);
    }
    limitOutReachability(reachability, ordering, out_ordering) {
        let resize_reachability = reachability.slice();
        let max_reachability = this.innerMaxReachability(reachability, ordering, out_ordering) * 1.1;
        for (let i = 0; i < out_ordering.length; i++) {
            let out_order = this.outOrderIndex(out_ordering[i], ordering);
            if (resize_reachability[out_order] > max_reachability) {
                resize_reachability[out_order] = max_reachability;
            }
        }
        return resize_reachability;
    };
    outOrderIndex(out_order, ordering) {
        let i = 0;
        for (; i < ordering.length; i++) {
            if (out_order == ordering[i]) {
                return i
            }
        }
        console.log("out_order is not in ordering")
        return 0
    }
    innerMaxReachability(reachability, ordering, out_ordering) {
        let max_reachability = 0
        for (let i = 0; i < reachability.length; i++) {
            if (out_ordering.includes(ordering[i])) {
                continue;
            } else {
                if (reachability[i] == "inf") {
                    max_reachability = Math.max(max_reachability, 0)
                } else {
                    max_reachability = Math.max(max_reachability, reachability[i])
                }
            }
        }
        return max_reachability
    };
    status() {
        super.status();
        console.log("OutOrdering:", this.out_ordering);
    }
}

function parseReachabilityJSON(reachability_json, mapboxmap) {
    return new OPTICSData(reachability_json["coordinates"], 
        reachability_json["reachability"], 
        reachability_json["ordering"],
        mapboxmap);
}

function drawPoints() {
    let obj = new GeojsonPointStructure(mapboxmap.map, 'GLHpoints', 'pink');
    obj.addStructure(optics_data.coodinatesToGeojson());
}
function drawClusters(eps) {
    let obj = new GeoJsonPolygonStructure(mapboxmap.map, 'clusters', 'None')
    obj.addStructure(optics_data.clustersToGeojson(eps));
}

var optics_data;
var mapboxmap;

function getReachability(g_mapboxmap, init_eps = 10) {
    let url = "http://localhost:8000/api/get_reachability"
    mapboxmap = g_mapboxmap;
    fetch(url, {
        mode: 'cors'
    }).then((response) => {
        return response.json();
    }).then((reach_json) => {
        optics_data = parseReachabilityJSON(reach_json);
        drawPoints();
        drawClusters(init_eps);
        updateReachability(init_eps);
    }).catch((e) => {
        console.log(e);
    });
};
function updateReachability(eps) {
    WIDTH = document.getElementById(ID).clientWidth - MARGIN;
    HEIGHT = document.getElementById(ID).clientHeight - MARGIN;
    let scope_data = optics_data.aggregateReachability();
    //scope_data.status();
    scope_data.reachabilityPlot("#d3plot", eps);
}

export { getReachability, updateReachability, drawClusters };