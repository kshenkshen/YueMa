#!/usr/bin/env python
# coding=utf8

import time
from oj import oj

code_str = '''import sys
class Point(object):
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b


def maxPoints2(points):
    MAX_INT = 1000000000
    mp = dict()
    res = points and 1 or 0

    for i in range(len(points)):
        points[i].x = float(points[i].x)
        points[i].y = float(points[i].y)

    for i in range(len(points)):
        mp.clear()
        mp[MAX_INT] = 0
        duplicate = 1
        for j in range(len(points)):
            if i == j:
                continue

            if points[i].x == points[j].x and points[i].y == points[j].y:
                duplicate += 1
                continue

            k = points[i].x == points[j].x and MAX_INT or ((points[i].y - points[j].y)/(points[i].x - points[j].x))
            if k in mp:
                mp[k] += 1
            else:
                mp[k] = 1
        for k in mp:
            mp[k] += duplicate
            res = max(mp[k], res)
    return res

if __name__ == "__main__":
    points = []
    for line in sys.stdin:
        l = line.split()
        points.append(Point(int(l[0]), int(l[1])))

    print maxPoints2(points)
'''

for i in range(3):
    print oj.random_pro(i)

req_dict = {'code': code_str, 'lang': 'py', u'pid': 3}

ret = oj.submit(req_dict)
print ret

time.sleep(2)

print oj.status(ret['fid'])
