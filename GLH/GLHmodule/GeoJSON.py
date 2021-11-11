class Geojson() :
    def __init__(self, name, list):
        self.geojson = {
            "type": "FeatureCollection",
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": self.makingFeature(list)
        }
    
    def makingFeature(self, list):
        features = []
        return features

class PointGeojson(Geojson) :
    def __init__(self, name, list):
        super().__init__(name, list)

    def makingFeature(self, list):
        features = []
        for item in list :
            # item[0],[1]: coordinate, item[2]: timestamp
            feature = {
                "type": "Feature",
                "properties": {
                    "timestamp" : item[2]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [item[0], item[1]]
                }
            }
            features.append(feature)
        return features

class LineGeojson(Geojson) :
    def __init__(self, name, coordinates):
        self.geojson = {
            "type": "LineString",
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "coordinates": coordinates
        }