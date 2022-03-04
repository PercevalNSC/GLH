// d3chart.js

class BarChartD3 {
    // dataset is 2 dimention array.
    constructor(dataset, width, height, padding) {
        this.dataset = dataset;
        this.width = width;
        this.height = height;
        this.padding = padding;
        console.log("plot size:", width, height);
    }
    initPlotArea(element_id) {
        d3.select(element_id).selectAll("svg").remove();
        return d3.select(element_id).append("svg").attr("width", this.width).attr("height", this.height);
    }
    setScale() {
        this.xScale = d3.scaleBand()
            .padding(0)
            .domain(this.dataset.map(function (d) { return d[0]; }))
            .range([this.padding, this.width - this.padding])
        this.yScale = d3.scaleSymlog()
            .domain([0, d3.max(this.dataset, function (d) { return d[1]; })])
            .range([this.height - this.padding, this.padding]);
    }
    addAxis(svg, ticks = 5){
        let offset = Math.floor(this.dataset.length / ticks)
        let xScale = this.xScale;
        let yScale = this.yScale;
        svg.append("g")
            .attr("transform", "translate(" + 0 + "," + (this.height - this.padding) + ")")
            .call(d3.axisBottom(xScale).tickValues(
                xScale.domain().filter(function (d, i) { return !(i % offset); })
            ));

        svg.append("g")
            .attr("transform", "translate(" + padding + "," + 0 + ")")
            .call(d3.axisLeft(yScale));
    }
    addPlot(svg){
        let xScale = this.xScale;
        let yScale = this.yScale;
        svg.append("g")
            .selectAll("rect")
            .data(this.dataset)
            .enter()
            .append("rect")
            .attr("x", function (d) { return xScale(d[0]); })
            .attr("y", function (d) { return yScale(d[1]); })
            .attr("width", xScale.bandwidth())
            .attr("height", function (d) { return this.height - this.padding - yScale(d[1]); })
            .attr("fill", "steelblue");
    }
    plot(element_id) {
        // element_id is html id to draw bar chart.

        var svg = this.initPlotArea(element_id);
        this.setScale();
        this.addAxis(svg, 5);
        this.addPlot(svg);

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
    constructor(reachability, width, height, padding) {
        super(reachability, width, height, padding);
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

        var yScale = d3.scaleSymlog()
            .domain([0, d3.max(this.dataset, function (d) { return d[1]; })])
            .range([this.height - this.padding, this.padding]);

        // d3.eventの座標をデータセットの範囲でマッピング
        var drag_yScale = d3.scaleLinear()
            .clamp(true)    //範囲外を丸める
            .domain([this.padding, this.height - this.padding])
            .range([this.padding, this.height - this.padding]);

        // epslineのdrag関数
        var drag = d3.drag()
            .on("drag", function () {
                d3.select(this).attr("y", drag_yScale(d3.event.y));
                update_eps();
            })
            .on("end", function () {
                console.log("drag end at:", drag_yScale(d3.event.y))
                update_eps();
            });

        this.svg.append("g")
            .append("rect")
            .attr("x", xScale(0))
            .attr("y", yScale(eps_height) - eps_line_width / 2)
            .attr("width", this.width - this.padding)
            .attr("height", eps_line_width)
            .attr("fill", "black")
            .call(drag)

        function update_eps() {
            let eps = yScale.invert(d3.event.y);
            mapboxmap.removeOPTICSLayer();
            drawClusters(eps)
        }
    }
}

export { BarChartD3, ReachabilityPlotD3, ReachabilityPlotWithEPS };