// d3plot.js

import { get_left_bottom, get_right_top } from "./Map.js"
import { PointGeoJson, PolygonGeoJson } from "./GeoJSON.js"
import { GeojsonPointStructure, GeoJsonPolygonStructure } from "./Structure.js"

let MARGIN = 8
let ID = "d3plot"
let WIDTH = document.getElementById(ID).clientWidth - MARGIN;
let HEIGHT = document.getElementById(ID).clientHeight - MARGIN;
let PADDING = 40;

class OPTICSData {
    constructor(coordinates, reachability, ordering) {
        this.coordinates = coordinates
        this.reachability = reachability
        this.ordering = ordering
    }
    reachability_plot(element_id, eps = 0) {
        let data = this.reachability
        let plot_obj = new ReachabilityPlotWithEPS(data, WIDTH, HEIGHT, PADDING);
        plot_obj.plot(element_id, eps);
    };
    map_scope(p0, p1) {
        console.log("map scope by", p0, p1);
        let coordinates = this.coordinates
        let reachability = this.reachability
        let ordering = this.ordering
        let zoom_coordinates = []
        let zoom_reachability = []
        let zoom_ordering = []
        let out_ordering = []
        let out_max_reachability = 0
        coordinates.forEach((coordinate, i) => {
            if (this._is_in_map(coordinate, p0, p1)) {
                if (out_max_reachability != 0) {
                    // add virtual point 
                    zoom_coordinates.push([0, 0]);
                    zoom_reachability.push(out_max_reachability);
                    zoom_ordering.push(ordering[i - 1]);
                    out_ordering.push(ordering[i - 1]);
                };
                // add in map point
                zoom_coordinates.push(coordinate);
                zoom_reachability.push(reachability[i]);
                zoom_ordering.push(ordering[i]);
                out_max_reachability = 0;
            } else {
                if (reachability[i] != "inf") {
                    out_max_reachability = Math.max(out_max_reachability, reachability[i]);
                }
                if (i == coordinate.length - 1) {
                    zoom_coordinates.push([0, 0]);
                    zoom_reachability.push(out_max_reachability);
                    zoom_ordering.push(ordering[i]);
                    out_ordering.push(ordering[i]);
                }
            };
        })
        return new ScopedOPTICSData(
            zoom_coordinates, zoom_reachability, zoom_ordering,
            out_ordering);
    };
    _is_in_map(coordinate, p0, p1) {
        let x = coordinate[0];
        let y = coordinate[1];
        if (p0[0] <= x && x <= p1[0] && p0[1] <= y && y <= p1[1]) {
            return true;
        } else {
            return false;
        };
    };

    // 降順の凸の高さのリスト
    maximaList(reachability) {
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

    outputClusters(eps){
        let polygons = []
        let cluster_points = []
        this.reachability.forEach((r, i) => {
            if (r <= eps) {
                cluster_points.push(this.coordinates[i]);
                if (i == this.reachability.length - 1) {
                    polygons.push(this._clusterToPolygon(cluster_points));
                };
            }else if (cluster_points.length != 0) {
                polygons.push(this._clusterToPolygon(cluster_points));
                cluster_points = [];
            } else {
                ;
            };
        })
        return polygons.filter(data => data != null);
    }
    _clusterToPolygon(cluster_points){
        let convexhull = d3.polygonHull(cluster_points);
        return convexhull
    }
    coodinatesToGeojson(){
        let geojsonobj = new PointGeoJson("GLHpoint",this.coordinates);
        return geojsonobj.geojson;
    }
    clustersToGeojson(eps){
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
        super(coordinates, reachability, ordering)
        this.out_ordering = out_ordering;
    };
    reachability_plot(element_id, eps = 0, map) {
        let data = this.resize_out_reachability(this.reachability, this.ordering, this.out_ordering);
        let plot_obj = new ReachabilityPlotWithEPS(data, WIDTH, HEIGHT, PADDING, map);
        plot_obj.plot(element_id, eps);
    }
    resize_out_reachability(reachability, ordering, out_ordering) {
        let resize_reachability = reachability.slice();
        let max_reachability = this.pure_max_reachability(reachability, ordering, out_ordering) * 1.1;
        for (let i = 0; i < out_ordering.length; i++) {
            let out_order = this.search_out_order(out_ordering[i], ordering);
            if (resize_reachability[out_order] > max_reachability) {
                resize_reachability[out_order] = max_reachability;
            }
        }
        return resize_reachability;
    };
    search_out_order(out_order, ordering) {
        let i = 0;
        for (; i < ordering.length; i++) {
            if (out_order == ordering[i]) {
                return i
            }
        }
        console.log("out_order is not in ordering")
        return 0
    }
    pure_max_reachability(reachability, ordering, out_ordering) {
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

class BarChartD3 {
    // dataset is 2 dimention array.
    constructor(dataset, width, height, padding) {
        this.dataset = dataset;
        this.width = width;
        this.height = height;
        this.padding = padding;
        console.log("plot size:", width, height);
    }
    plot(element_id) {
        // element_id is html id to draw bar chart.
        let width = this.width
        let height = this.height
        let padding = this.padding
        let ticks = 5;
        let offset = Math.floor(this.dataset.length / ticks)

        d3.select(element_id).selectAll("svg").remove();
        var svg = d3.select(element_id).append("svg").attr("width", width).attr("height", height);

        // setting axis scale

        var xScale = d3.scaleBand()
            .padding(0)
            .domain(this.dataset.map(function (d) { return d[0]; }))
            .range([padding, width - padding])

        var yScale = d3.scaleLinear()
            .domain([0, d3.max(this.dataset, function (d) { return d[1]; })])
            .range([height - padding, padding]);

        // draw axis
        svg.append("g")
            .attr("transform", "translate(" + 0 + "," + (height - padding) + ")")
            .call(d3.axisBottom(xScale).tickValues(
                xScale.domain().filter(function (d, i) { return !(i % offset); })
            ));

        svg.append("g")
            .attr("transform", "translate(" + padding + "," + 0 + ")")
            .call(d3.axisLeft(yScale));

        // draw bar
        svg.append("g")
            .selectAll("rect")
            .data(this.dataset)
            .enter()
            .append("rect")
            .attr("x", function (d) { return xScale(d[0]); })
            .attr("y", function (d) { return yScale(d[1]); })
            .attr("width", xScale.bandwidth())
            .attr("height", function (d) { return height - padding - yScale(d[1]); })
            .attr("fill", "steelblue");

        return svg;
    };
    status() {
        console.log(this.dataset);
        console.log(this.width, this.height, this.padding);
    }
}
class ReachabilityPlotD3 extends BarChartD3 {
    // reachability is 1 dimmention list.
    constructor(reachability, width, height, padding) {
        let dataset = reachability.map(function (v, i) { return (v == "inf" ? [i, 0] : [i, v]); });
        super(dataset, width, height, padding);
    }
}
class ReachabilityPlotWithEPS extends ReachabilityPlotD3 {
    constructor(reachability, width, height, padding, map) {
        super(reachability, width, height, padding);
        this.map = map;
    }
    plot(element_id, eps_height = 0) {
        this.svg = super.plot(element_id);
        this.add_eps_line(eps_height);
    }
    add_eps_line(eps_height = 0) {
        let eps_line_width = 5

        var xScale = d3.scaleBand()
            .padding(0)
            .domain(this.dataset.map(function (d) { return d[0]; }))
            .range([this.padding, this.width - this.padding])

        var yScale = d3.scaleLinear()
            .domain([0, d3.max(this.dataset, function (d) { return d[1]; })])
            .range([this.height - this.padding, this.padding]);

        // d3.eventの座標をデータセットの範囲でマッピング
        var drag_yScale = d3.scaleLinear()
            .clamp(true)    //範囲外を丸める
            .domain([this.padding, this.height - this.padding])
            .range([d3.max(this.dataset, function (d) { return d[1]; }), 0])

        var map = this.map;
        // epslineのdrag関数
        var drag = d3.drag()
            .on("drag", function () {
                d3.select(this).attr("y", yScale(drag_yScale(d3.event.y)));
            })
            .on("end", function () {
                map.removeLayer("clustersoutline")
                map.removeSource("clusters")
                let eps = drag_yScale(d3.event.y)
                console.log("drag end:", eps);
                drawClusters(map, eps)
            });

        this.svg.append("g")
            .append("rect")
            .attr("x", xScale(0))
            .attr("y", yScale(eps_height) - eps_line_width / 2)
            .attr("width", this.width - this.padding)
            .attr("height", eps_line_width)
            .attr("fill", "black")
            .call(drag)
    }
}

var optics_data

function get_reachability(map) {
    let url = "http://localhost:8000/api/get_reachability"
    fetch(url, {
        mode: 'cors'
    }).then((response) => {
        return response.json();
    }).then((reach_json) => {
        let init_eps = 10;
        optics_data = new OPTICSData(reach_json["coordinates"], reach_json["reachability"], reach_json["ordering"]);
        drawPoints(map);
        //optics_data.status()
        //console.log("pick boundary:", optics_data.pick_boundary(optics_data.reachability))
        drawClusters(map, init_eps);
        update_reachability(map, init_eps);
    }).catch((e) => {
        console.log(e);
    });
};
function update_reachability(map, eps) {
    let p0 = get_left_bottom(map);
    let p1 = get_right_top(map);
    let scope_data = optics_data.map_scope(p0, p1);
    //scope_data.status();
    scope_data.reachability_plot("#d3plot", eps, map);
}

function drawPoints(map){
    let obj = new GeojsonPointStructure(map, "GLHpoints", "pink");
    obj.add_structure(optics_data.coodinatesToGeojson());
}
function drawClusters(map, eps) {
    let obj = new GeoJsonPolygonStructure(map, "clusters", "None")
    obj.add_structure(optics_data.clustersToGeojson(eps));
}

export { get_reachability, update_reachability, drawClusters};