import GLH.GLHmodule.Clustering as gc
import math

a1 = [36.1037, 140.0878]
a2 = [35.6550, 139.7447]
dist = math.sqrt((a1[0] - a2[0])**2 +  (a1[1] - a2[1])**2)
real_dist = 58.643
print(dist)
print(real_dist)
print(gc.geography_to_euclid(real_dist))
print(gc.euclid_to_geography(dist))
print(gc.geography_to_euclid(2))

from GLH.GLHmodule.geo2 import getBoundsAt

center = [139.545, 35.655]
zoom = 15
size = [720, 720]

print(getBoundsAt(center, zoom, size))