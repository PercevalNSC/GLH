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

    plot(element_id) {
        // element_id is html id to draw bar chart.
        this.svg = this._initPlotArea(element_id);
        this._setScale();
        this._addAxis(5);
        this._addPlot();
    };

    _initPlotArea(element_id) {
        d3.select(element_id).selectAll("svg").remove();
        return d3.select(element_id).append("svg").attr("width", this.width).attr("height", this.height);
    }
    _setScale() {
        this.xScale = d3.scaleBand()
            .padding(0)
            .domain(this.dataset.map(function (d) { return d[0]; }))
            .range([this.padding, this.width - this.padding])
        this.yScale = d3.scaleSymlog()
            .domain([0, d3.max(this.dataset, function (d) { return d[1]; })])
            .range([this.height - this.padding, this.padding]);
    }
    _addAxis(ticks = 5) {
        let offset = Math.floor(this.dataset.length / ticks)
        this.svg.append("g")
            .attr("transform", "translate(" + 0 + "," + (this.height - this.padding) + ")")
            .call(d3.axisBottom(this.xScale).tickValues(
                this.xScale.domain().filter(function (d, i) { return !(i % offset); })
            ));

       this.svg.append("g")
            .attr("transform", "translate(" + this.padding + "," + 0 + ")")
            .call(d3.axisLeft(this.yScale));
    }
    _addPlot() {
        let xScale = this.xScale;
        let yScale = this.yScale;
        let plot_height = this.height - this.padding;
        this.svg.append("g")
            .selectAll("rect")
            .data(this.dataset)
            .enter()
            .append("rect")
            .attr("x", function (d) { return xScale(d[0]); })
            .attr("y", function (d) { return yScale(d[1]); })
            .attr("width", xScale.bandwidth())
            .attr("height", function (d) { return plot_height - yScale(d[1]); })
            .attr("fill", "steelblue");
    }
    
    status() {
        console.log("Dataset:", this.dataset);
        console.log("Width:", this.width, "Height:", this.height, "Padding:", this.padding);
    }
}

class ReachabilityPlotD3 extends BarChartD3 {
    // reachability is 1 dimmention list.
    constructor(reachability, width, height, padding) {
        //remove inf in reachability
        let dataset = reachability.map(function (v, i) { return (v == "inf" ? [i, 0] : [i, v]); });

        super(dataset, width, height, padding);
    }
}

class ReachabilityPlotWithEPS extends ReachabilityPlotD3 {
    constructor(reachability, width, height, padding) {
        super(reachability, width, height, padding);
        this.eps_line_width = 5;
    }
    plot(element_id, eps_height = 0) {
        super.plot(element_id);
        this._addEpsLine(eps_height);
    }
    _addEpsLine(eps_height = 0) {
        var drag = this._dragFunction();
        this._addLine(drag, eps_height);
    }
    _dragFunction() {
        let yScale = this.yScale;
        var drag_yScale = d3.scaleLinear()
            .clamp(true)    //範囲外を丸める
            .domain([this.padding, this.height - this.padding])
            .range([this.padding, this.height - this.padding]);

        return d3.drag()
            .on("drag", function () {
                d3.select(this).attr("y", drag_yScale(d3.event.y));
            })
            .on("end", function () {
                console.log("drag end at:",  yScale.invert(d3.event.y))
            });
    }
    _addLine(drag, eps_height) {
        this.svg.append("g")
            .append("rect")
            .attr("x", this.xScale(0))
            .attr("y", this.yScale(eps_height) - this.eps_line_width / 2)
            .attr("width", this.width - this.padding)
            .attr("height", this.eps_line_width)
            .attr("fill", "black")
            .call(drag)
    }
}

export { BarChartD3, ReachabilityPlotD3, ReachabilityPlotWithEPS };