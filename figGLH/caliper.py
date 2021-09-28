# キャリパー法(Rotating Calipers法)
# 凸多角形を回転しながら走査し、最遠点対を求める
# https://tjkendev.github.io/procon-library/python/geometry/rotating_calipers.html

from math import sqrt
from geo2 import distance as g2distance

def cross(a, b, c, d):
    return (b[0]-a[0])*(d[1]-c[1]) - (b[1]-a[1])*(d[0]-c[0])
# グラハムスキャン
def convex_hull(ps):
    qs = []
    n = len(ps)
    for p in ps:
        while len(qs)>1 and cross(qs[-1], qs[-2], qs[-1], p) > 0:
            qs.pop()
        qs.append(p)
    t = len(qs)
    for i in range(n-2, -1, -1):
        p = ps[i]
        while len(qs)>t and cross(qs[-1], qs[-2], qs[-1], p) >= 0:
            qs.pop()
        qs.append(p)
    return qs

def dist(a, b):
    # return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return g2distance(a,b)
# キャリパー法
def rotating_calipers(ps):
    ps.sort()
    qs = convex_hull(ps)
    n = len(qs)
    if n == 2:
        return dist(qs[0], qs[1])
    i = j = 0
    for k in range(n):
        if qs[k] < qs[i]: i = k
        if qs[j] < qs[k]: j = k
    res = 0
    si = i; sj = j
    c = 0
    while i != sj or j != si:
        res = max(res, dist(qs[i], qs[j]))
        if res >= dist(qs[i], qs[j]) :
            c += 1
        else :
            res = dist(qs[i], qs[j])
        if c == 30 :
            res = 0
            print(qs)
            print("break")
            break
        if cross(qs[i], qs[i-n+1], qs[j], qs[j-n+1]) < 0:
            i = (i + 1) % n
        else:
            j = (j + 1) % n
    return res

def gravityPointDistance(points):
    res = 0
    gravity_point = [0, 0]
    for point in points:
        assert len(point) == len(gravity_point), "len(point) is not equal 2"
        for index in range(len(gravity_point)):
            gravity_point[index] = (gravity_point[index] + point[index])
    gravity_point = [ x / len(points) for x in gravity_point]
    for point in points :
        dist = g2distance(point, gravity_point) * 1000
        # print(dist)
        res = max(res, dist * 2)
    return res

if __name__ == "__main__" :
    points = [[35.6571999, 139.5420565], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.6571999, 139.5420565]]

    print(gravityPointDistance(points))

    points = [[35.6575643, 139.5419497],[35.65615972142857, 139.5442210142857]]
    print(g2distance(*points))

    points = [[35.1, 139.1], [35.1, 138.9], [34.9, 139.1], [34.9, 138.9]]

    print(gravityPointDistance(points))

    print(g2distance([35.1, 139.1], [34.9, 138.9]) * 1000)