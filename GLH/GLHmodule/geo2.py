# coding: utf-8
import math

def fromLngLatToPoint(lng, lat):
  return [(float(lng) + 180) / 360 * 512, 
    ((1 - math.log(math.tan(float(lat) * math.pi / 180) + 1 / math.cos(float(lat) * math.pi / 180)) / math.pi) / 2) * 512]

def fromPointToLngLat(x, y):
  n = math.pi - 2 * math.pi * float(y) / 512
  return [float(x) / 512 * 360 - 180, (180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))]

def fromPointToPixel(x, y, z):
  return [float(x) * math.pow(2, z), float(y) * math.pow(2, z)]

def fromPixelToPoint(x, y, z):
  return [float(x) * math.pow(2, -z), float(y) * math.pow(2, -z)]

def fromLngLatToPixel(lng, lat, z):
  return [(float(lng) + 180) / 360 * 512 * math.pow(2, z), 
    ((1 - math.log(math.tan(float(lat) * math.pi / 180) + 1 / math.cos(float(lat) * math.pi / 180)) / math.pi) / 2) * 512 * math.pow(2, z)]

def fromPixelToLngLat(x, y, z):
  n = math.pi - 2 * math.pi * float(y) * math.pow(2, -z) / 512
  return [float(x) * math.pow(2, -z) / 512 * 360 - 180, (180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))]

def project(lngLat, centerLngLat, z, size):
  c = fromLngLatToPixel(centerLngLat[0], centerLngLat[1], z)
  p = fromLngLatToPixel(lngLat[0], lngLat[1], z)
  return [float(size[0]/2) - c[0] + p[0], float(size[1]/2) - c[1] + p[1]]

def unproject(p, centerLngLat, z, size):
  c = fromLngLatToPixel(centerLngLat[0], centerLngLat[1], z)
  return fromPixelToLngLat(c[0] - float(size[0]) / 2  + p[0], c[1] - float(size[1]) / 2 + p[1], z) 

def projectMany(lngLats, centerLngLat, z, size):
  c = fromLngLatToPixel(centerLngLat[0], centerLngLat[1], z)
  return [[float(size[0]/2) - c[0] + p[0], float(size[1]/2) - c[1] + p[1]] for p in [fromLngLatToPixel(lngLat[0], lngLat[1], z) for lngLat in lngLats]]

def unprojectMany(pxs, centerLngLat, z, size):
  c = fromLngLatToPixel(centerLngLat[0], centerLngLat[1], z)
  return [fromPixelToLngLat(c[0] - float(size[0]) / 2  + p[0], c[1] - float(size[1]) / 2 + p[1], z) for p in pxs]

def getBoundsAt(center :list, z :int, size :list):
  """
  return [left_down[lng, lat], right_up[lng, lat]]

  center : center latlng of map
  z : zoom level
  size : window size [width, height]
  """
  d = [float(size[0]) / (2 * math.pow(2, z)), float(size[1]) / (2 * math.pow(2, z))]
  p = fromLngLatToPoint(*center)
  return [fromPointToLngLat(p[0] - d[0], p[1] + d[1]), fromPointToLngLat(p[0] + d[0], p[1] - d[1])]

def getCenterFromBounds(bounds):
  """
  return center_lnglat

  bounds: 2 lnglat of window corner
  """
  p0 = fromLngLatToPoint(*bounds[0])
  p1 = fromLngLatToPoint(*bounds[1])
  return fromPointToLngLat((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)

def getZoomAndCenterToFitBounds(bounds, size):
  p0 = fromLngLatToPoint(*bounds[0])
  p1 = fromLngLatToPoint(*bounds[1])
  return [int(math.floor(min(math.log(size[0] / (p1[0] - p0[0]), 2), math.log(size[1] / (p0[1] - p1[1]), 2)))), 
    fromPointToLngLat((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)]

def pointInRect(p, v1, v2):
  return (v1[0] - p[0]) * (v2[0] - p[0]) <= 0 and (v1[1] - p[1]) * (v2[1] - p[1]) <= 0

def visibleZoom(lngLat1, lngLat2, pixelLength):
  return math.log(math.pow(pixelLength, 2) / (math.pow(float(lngLat1[0] - lngLat2[0]) / 360 * 512, 2) + math.pow((math.log(math.tan(float(lngLat1[1]) * math.pi / 180) + 1 / math.cos(float(lngLat1[1]) * math.pi / 180)) - math.log(math.tan(float(lngLat2[1]) * math.pi / 180) + 1 / math.cos(float(lngLat2[1]) * math.pi / 180)) ) / math.pi / 2 * 512, 2)) , 4)

def distance(lngLat1, lngLat2):
  a = math.pow(math.sin((lngLat1[1] -lngLat2[1]) * math.pi / 360), 2) + math.pow(math.sin((lngLat1[0] -lngLat2[0]) * math.pi / 360), 2) * math.cos(lngLat1[1] * math.pi / 180) * math.cos(lngLat2[1] * math.pi / 180)
  return 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) * 6373 # distance in km

def totalDistance(lngLatList):
  d = 0.0
  for i in range(len(lngLatList) - 1):
    d = d + distance(lngLatList[i], lngLatList[i + 1])
  return d


if __name__ == '__main__' :
  center = (35.665875010721926, 139.70534033813476)
  zoom=12
  size=(1600, 900)
  print(center)
  print(fromLngLatToPoint(*center))
  print(fromLngLatToPixel(center[0], center[1], zoom))
  print(getBoundsAt(center, zoom, size))
  print(getCenterFromBounds(getBoundsAt(center, zoom, size)))
  print(getZoomAndCenterToFitBounds(getBoundsAt(center, zoom, size), size))

#[35.79129300629037, 139.43068213500976] [35.79129300629037, 139.97999854125976]
#                      (35.665875010721926, 139.70534033813476)
#[35.540259679943496, 139.43068213500976] [35.540259679943496, 139.97999854125976]
