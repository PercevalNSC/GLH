import {DrawPoints, DrawLine, DrawPolygon} from "./modules/Structure.js"

function asSrpPoint(map, color = "blue", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/activitySegment.simplifiedRawPath"
    let as_srp_point = new DrawPoints(map, url, "AsSrp");
    as_srp_point.color = color
    as_srp_point.visibility = visibility
    as_srp_point.addStructure();
}
function asWpPoint(map, color = "pink", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/activitySegment.waypointPath"
    let as_wp_point = new DrawPoints(map, url, "AsWp");
    as_wp_point.color = color;
    as_wp_point.visibility = visibility;
    as_wp_point.addStructure();
}
function pvSrpPoint(map, color = "yellow", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/placeVisit.simplifiedRawPath"
    let pv_srp_point = new DrawPoints(map, url, "PvSrp");
    pv_srp_point.color = color;
    pv_srp_point.visibility = visibility;
    pv_srp_point.addStructure();
}
function pvLocationPoint(map, color = "white", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/placeVisit.location"
    let pv_location = new DrawPoints(map, url, "PvLoc", color, 6, 1, visibility);
    pv_location.addStructure();
}
function dbscan_point(map, color = "red", visibility = "visible") {
    let url = "http://localhost:8000/api/geojson/point/dbscan"
    let dbscan_point = new DrawPoints(map, url, "dbscan_point");
    dbscan_point.color = color;
    dbscan_point.visibility = visibility;
    dbscan_point.addStructure();
}

function add_routepath(map, color = 'gray', visibility = "visible", opacity = 0.5, width = 1) {
    let url = "http://localhost:8000/api/geojson/line/route"
    let id = "routepath"
    let routepath = new DrawLine(map, url, id, color, width, opacity, visibility);
    routepath.addStructure();
}

function dbscan_polygon(map, fillcolor = "None", linecolor = "black") {
    let url = "http://localhost:8000/api/geojson/polygon/dbscan"
    let id = "dbscan_polygon"
    let dbscan_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 3, 0.5)
    dbscan_polygon.addStructure();
}
function optics_polygon(map, eps = 1.0, fillcolor = "None", linecolor = "black") {
    let url = "http://localhost:8000/api/geojson/polygon/optics/" + eps.toFixed(10)
    let id = "optics_polygon"
    let optics_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 3, 0.6);
    optics_polygon.addStructure();
}
function viewport_polygon(map, fillcolor = "None", linecolor = "gray") {
    let url = "http://localhost:8000/api/geojson/viewport";
    let id = "viewport";
    let viewport_polygon = new DrawPolygon(map, url, id, fillcolor, linecolor, 2, 0.3);
    viewport_polygon.addStructure();
}

export {asSrpPoint, asWpPoint, pvSrpPoint, pvLocationPoint,
    dbscan_point, add_routepath, dbscan_polygon, optics_polygon,
    viewport_polygon};