# キャリパー法(Rotating Calipers法)
# 凸多角形を回転しながら走査し、最遠点対を求める
# https://tjkendev.github.io/procon-library/python/geometry/rotating_calipers.html

from math import sqrt

def rotating_calipers(ps):
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
    while i != sj or j != si:
        res = max(res, dist(qs[i], qs[j]))
        if cross4(qs[i], qs[i-n+1], qs[j], qs[j-n+1]) < 0:
            i = (i + 1) % n
        else:
            j = (j + 1) % n
    return res

def dist(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def cross4(a, b, c, d):
    return (b[0]-a[0])*(d[1]-c[1]) - (b[1]-a[1])*(d[0]-c[0])
def cross3(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

# ps = [(x, y), ...]: ソートされた座標list
def convex_hull(ps):
    qs = []
    N = len(ps)
    for p in ps:
        # 一直線上で高々2点にする場合は ">=" にする
        while len(qs) > 1 and cross3(qs[-1], qs[-2], p) > 0:
            qs.pop()
        qs.append(p)
    t = len(qs)
    for i in range(N-2, -1, -1):
        p = ps[i]
        while len(qs) > t and cross3(qs[-1], qs[-2], p) > 0:
            qs.pop()
        qs.append(p)
    return qs

if __name__ == "__main__" :
    points = [[0,0], [2,1], [3,2], [1,4]]

    print(rotating_calipers(points))