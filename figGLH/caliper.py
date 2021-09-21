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
    return g2distance(a,b) # kmで計算
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
    gravity_point_sum = [0, 0]
    for length, point in enumerate(points,1):
        assert len(point) == len(gravity_point), "len(point) is not equal 2"
        for index in range(len(gravity_point)):
            gravity_point_sum[index] = (gravity_point_sum[index] + point[index])
        gravity_point = [ x / (length) for x in gravity_point_sum]
        res = max(res, dist(gravity_point, point))
        #print(point, gravity_point, res)
    return res

if __name__ == "__main__" :
    points = [[35.6571999, 139.5420565], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.6582316, 139.5421605], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.658933, 139.5424788], [35.6571999, 139.5420565]]

    print(gravityPointDistance(points))