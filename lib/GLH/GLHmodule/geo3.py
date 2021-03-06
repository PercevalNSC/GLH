# coding: utf-8
# Author: Keita Watanabe(UEC, Fujita Lab)
# version: 0.1.1(alpha.block1)

import math

#緯度経度オブジェクト
class Coordinate :
    def __init__(self, lng, lat):
        self.lng = float(lng)
        self.lat = float(lat)
    
    def toPoint(self):
        return [(self.lng + 180) / 360 * 512, 
            ((1 - math.log(math.tan(self.lat * math.pi / 180) + 1 / math.cos(self.lat * math.pi / 180)) / math.pi) / 2) * 512]
    
    def toPixel(self, z):
        return [(self.lng + 180) / 360 * 512 * math.pow(2, z), 
            ((1 - math.log(math.tan(self.lat * math.pi / 180) + 1 / math.cos(self.lat * math.pi / 180)) / math.pi) / 2) * 512 * math.pow(2, z)]

    def print(self):
        print([self.lng, self.lat])

class Point :
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def toLngLat(self):
        n = math.pi - 2 * math.pi * self.y / 512
        return [self.x / 512 * 360 - 180, (180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))]
    def toPixel(self, z):
        return [self.x * math.pow(2, z), self.y * math.pow(2, z)]


class Pixel :
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = z
    
    def toPoint(self):
        return [self.x * math.pow(2, - self.z), self.y * math.pow(2, - self.z)]

    def toLngLat(self):
        n = math.pi - 2 * math.pi * self.y * math.pow(2, - self.z) / 512
        return [self.x * math.pow(2, - self.z) / 512 * 360 - 180, (180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))]

TOKYO_1LNG = (1.51985 + 1.85225) * 30
TOKYO_1LNG1 = 1.51985 * 60
TOKYO_1LNG2 = 1.85225 * 60

def euclid_to_geography(euclid_dist):
    return euclid_dist * TOKYO_1LNG #(km)

def geography_to_euclid(geography_dist):
    # input (km)
    return geography_dist / TOKYO_1LNG
