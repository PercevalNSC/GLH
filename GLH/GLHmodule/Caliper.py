# キャリパー法(Rotating Calipers法)
# 凸多角形を回転しながら走査し、最遠点対を求める
# https://tjkendev.github.io/procon-library/python/geometry/rotating_calipers.html

from math import sqrt
from .geo2 import distance as g2distance
import time

# グラハムスキャン
def convex_hull(points):
    # pointsを辞書順かつ非重複にする
    points.sort()
    points = get_unique_list(points)

    conv_points = []
    n = len(points)
    for p in points:
        while len(conv_points)>1 and cross(conv_points[-1], conv_points[-2], conv_points[-1], p) > 0:
            conv_points.pop()
        conv_points.append(p)
    t = len(conv_points)
    for i in range(n-2, -1, -1):
        p = points[i]
        while len(conv_points)>t and cross(conv_points[-1], conv_points[-2], conv_points[-1], p) >= 0:
            conv_points.pop()
        conv_points.append(p)
    return conv_points

#　順序保持・非重複にした2次元のリストを返す
def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def dist(a, b):
    # return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return g2distance(a,b)

def cross(a, b, c, d):
    return (b[0]-a[0])*(d[1]-c[1]) - (b[1]-a[1])*(d[0]-c[0])

# キャリパー法
def rotating_calipers(points):
    conv_points = convex_hull(points)
    n = len(conv_points)
    if n == 2: return dist(conv_points[0], conv_points[1])
    
    i = j = 0
    for k in range(n):
        if conv_points[k] < conv_points[i]: i = k
        if conv_points[j] < conv_points[k]: j = k
    #print(min_index, max_index)
    distance = 0
    min_index = i; max_index = j
    start = time.time()
    while i != max_index or j != min_index:
        assert time.time() - start < 10, "caliper timeout"
        distance = max(distance, dist(conv_points[i], conv_points[j]))
        if cross(conv_points[i], conv_points[i-n+1], conv_points[j], conv_points[j-n+1]) < 0:
            i = (i + 1) % n
        else:
            j = (j + 1) % n
    return distance

# 重心と最遠点の距離
def gravityPointDistance(points):
    max_dist = 0
    gravity_point = [0, 0]
    for point in points:
        assert len(point) == len(gravity_point), "len(point) is not equal 2"
        for index in range(len(gravity_point)):
            gravity_point[index] = (gravity_point[index] + point[index])
    gravity_point = [ x / len(points) for x in gravity_point]

    for point in points :
        dist = g2distance(point, gravity_point) * 1000
        max_dist = max(max_dist, dist * 2)
    return max_dist



if __name__ == "__main__" :
    points = [[35.6571999, 139.5420565], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.6571999, 139.5420565]]

    print(convex_hull(points))

    rotating_calipers(points)