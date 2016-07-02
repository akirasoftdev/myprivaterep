# -*- coding: utf-8 -*-
import os
import re

files_map = {
    '0': os.listdir('./work/0'),
    '1': os.listdir('./work/1'),
    '2': os.listdir('./work/2'),
    '3': os.listdir('./work/3'),
    '4': os.listdir('./work/4'),
    '5': os.listdir('./work/5'),
    '6': os.listdir('./work/6'),
    '7': os.listdir('./work/7'),
    '8': os.listdir('./work/8'),
    '9': os.listdir('./work/9'),
    'a': os.listdir('./work/A'),
    'b': os.listdir('./work/B'),
    'c': os.listdir('./work/C'),
    'd': os.listdir('./work/D'),
    'e': os.listdir('./work/E'),
    'f': os.listdir('./work/F'),
    'g': os.listdir('./work/G')
}

min_w = 999
max_w = 0
min_h = 999
max_h = 0
min_area = 999.0
max_area = 0.0
min_cx = 999.0
max_cx = 0.0
min_cy = 999.0
max_cy = 0.0
size_map = {}

for key, files in files_map.items():
    for file in files:
        w, h, area, cx, cy = re.compile('^(\d+)\-(\d+)_(\d+\.\d)_(\d+\.\d+)\-(\d+.\d+).*$').search(file).groups()
        min_w = min(int(w), min_w)
        max_w = max(int(w), max_w)
        min_h = min(int(h), min_h)
        max_h = max(int(h), min_h)
        min_area = min(float(area), min_area)
        max_area = max(float(area), max_area)
        min_cx = min(float(cx), min_cx)
        max_cx = max(float(cx), max_cx)
        min_cy = min(float(cy), min_cy)
        max_cy = max(float(cy), max_cy)
        size = '%s-%s_%s_%s-%s' % (w,h,area,cx,cy)
        if size in size_map:
            if key in size_map[size]:
                size_map[size][key] += 1
            else:
                size_map[size][key] = 1
        else:
            size_map[size] = {}
            size_map[size][key] = 1

print('min_w = ' + str(min_w))
print('max_w = ' + str(max_w))
print('min_h = ' + str(min_h))
print('max_h = ' + str(max_h))
print('min_area = ' + str(min_area))
print('max_area = ' + str(max_area))
print('min_cx = ' + str(min_cx))
print('max_cx = ' + str(max_cx))
print('min_cy = ' + str(min_cy))
print('max_cy = ' + str(max_cy))

for key, value in size_map.items():
    if len(value) > 1:
        for a, b in value.items():
            print("%s : %s, %d" % (key, a, b))
        raise Exception()

    for a, b in value.items():
        print("%s : %s, %d" % (key, a, b))
