from GLH.GLHmodule.geo2 import getBoundsAt

center = [139.545, 35.655]
zoom_range = [7,15]
size = [ 1536, 807 ]

print("Center:", center)
print("Window Size:", size)
for z in range(zoom_range[0], zoom_range[1]+1, 1):
    print("zoom:", z, "corner:", getBoundsAt(center, z, size))