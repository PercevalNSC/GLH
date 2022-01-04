// d3plot.js
let WIDTH = document.getElementById("d3plot").clientWidth;
let HEIGHT = document.getElementById("d3plot").clientHeight;
let PADDING = 30;

class OPTICSData {
    constructor(coordinates, reachability, ordering){
        this.coordinates = coordinates
        this.reachability = reachability
        this.ordering = ordering
    }
    reachability_plot(element_id){
        let data = this.reachability
        let temp1 = new ReachabilityPlotD3(
            data, WIDTH, HEIGHT, PADDING);
        temp1.plot(element_id);
    }
    map_scope(p0, p1){
        let coordinates = this.coordinates
        let reachability = this.reachability
        let ordering = this.ordering
        let zoom_coordinates = []
        let zoom_reachability = []
        let zoom_ordering = []
        let out_reachability = []
        let out_ordering = []
        let skipcount = 0
        for (let i = 0; i < this.coordinates.length ; i++) {
            if (skipcount > 0) {
                skipcount--;
                continue;
            }
            if (this._is_in_map(p0, p1)) {
                zoom_coordinates.push(coordinates[i]);
                zoom_reachability.push(reachability[i]);
            } else {
                temp = this._not_in_map(i, p0, p1);
                skipcount = temp[0]
                zoom_coordinates.push([0, 0])
                zoom_reachability.push(0)
                out_reachability.push(temp[1])
                out_ordering.push(ordering[i])
            }
            zoom_ordering.push(ordering[i]);
        }
        return new ScopedOPTICSData(
            zoom_coordinates, zoom_reachability, zoom_ordering,
            out_reachability, out_ordering);
    }
    _is_in_map(coordinate, p0, p1){
        let x = coordinate[0];
        let y = coordinate[1];
        if (p0[0] < x < p1[0] && p0[1] < y < p1[1]) {
            return true;
        } else {
            return false;
        };
    };
    _not_in_map(start_index, p0, p1){
        let max_reachability = 0;
        let coordinates = this.coordinates
        let reachability = this.reachability
        for(let i = start_index; i < coordinates.length; i++){
            if (this._is_in_map(coordinates[i], p0, p1)) {
                break;
            }else {
                max_reachability = Math.max(
                    max_reachability, reachability[i]);
            }
        }
        skipcount = i - start_index + 1;
        return [skipcount, max_reachability];
    };
    status(){
        console.log(this.coordinates);
        console.log(this.reachability);
        console.log(this.ordering);
    }
}
class ScopedOPTICSData extends OPTICSData {
    constructor(coordinates, reachability, ordering, out_reachability, out_ordering){
        super(coordinates, reachability, ordering)
        this.out_reachability = out_reachability;
        this.out_ordering = out_ordering;
    }
}

class BarChartD3 {
    // dataset is 2 dimmention array.
    constructor(dataset, width, height, padding) {
        this.dataset = dataset;
        this.width = width;
        this.height = height;
        this.padding = padding;
    }
    plot(element_id) {
        // element_id is html id to draw bar chart.
        let width = this.width
        let height = this.height
        let padding = this.padding

        var svg = d3.select(element_id).append("svg").attr("width", width).attr("height", height);

        // setting axis scale
        let ticks = 5;
        let offset = Math.floor(this.dataset.length / ticks)
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
                xScale.domain().filter(function(d,i){ return !(i%offset) ;})
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
            .attr("fill", "black");
    };
    status(){
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

function get_reachability(){
    url = "http://localhost:8000/api/get_reachability"
    fetch(url, {
        mode: 'cors'
    }).then((response) => {
        return response.json();
    }).then((reach_json) => {
        let temp = new OPTICSData(reach_json["coordinates"], reach_json["reachability"], reach_json["ordering"]);
        temp.reachability_plot("#d3plot")
    }).catch((e) => {
        console.log(e);
    });
};

console.log("d3 neko");
get_reachability()
