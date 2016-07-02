#coding:utf-8
import numpy as np
import copy
import cv2
import pylab as plt

class CharPos(object):
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self.next = None
        self.prev = None

size_of_charmap = {
    '0':(1, [(351.5, 7, 13), (357.5, 7, 13), (358.5, 7, 13), (359.5, 7, 13), (379.5, 8, 13), (380.5, 8, 13),
             (381.5, 8, 13), (385.5, 8, 13), (386.5, 8, 13)]),
    '1':(0, [(118.5, 5, 13), (119.5, 5, 13), (122.5, 6, 13), (122.5, 5, 13), (123.5, 6, 13), (123.5, 5, 13),
             (145.5, 6, 13)]),
    '2':(0, [(193.5, 6, 14), (193.5, 7, 14), (194.5, 7, 14), (197.5, 7, 14), (200.5, 7, 14), (207.5, 7, 14),
              (208.5, 7, 14), (209.5, 7, 14), (210.5, 7, 14), (212.5, 7, 14), (213.5, 7, 14), (217.5, 7, 14)]),
    '3':(0, []),
    '4':(1, [(237.0, 9, 14)]),
    '5':(0, [(219.0, 7, 13), (223.0, 7, 13), (224.0, 7, 13), (227.0, 7, 13), (230.0, 7, 13), (236.0, 8, 13),
             (236.0, 7, 13), (239.0, 8, 13), (241.0, 7, 13)]),
    '6':(1, [(301.0, 7, 15), (312.0, 7, 15)]),
    '7':(0, [(147.5, 7, 10), (164.5, 8, 11)]),
    '8':(2, [(329.0, 7, 14), (332.0, 7, 14), (353.0, 8, 14), (356.0, 8, 14), (357.0, 8, 14)]),
    '9':(1, []),
    'A':(1, []),
    'B':(2, []),
    'C':(0, []),
    'D':(1, [(362.5, 6, 13), (363.5, 6, 13), (364.5, 6, 13), (365.5, 6, 13), (385.5, 7, 13), (386.5, 7, 13),
             (388.5, 7, 13), (390.5, 7, 13), (392.5, 7, 13), (393.5, 7, 13)]),
}
min_val = 99999
max_val = 0

def count_child(hierarcy, index):
    count = 0
    next,_,child,_ = hierarchy[0][index]
    if child == -1:
        return 0
    next = child
    while next != -1:
        next,_,child,_ = hierarcy[0][next]
        if child != -1:
            return -1
        count += 1
    return count

def find_char(size, cx, cy, hierarcy, index):
    if min_val <= size <= max_val:
        for char, (num_child, char_size_list) in size_of_charmap.items():
            if (size, cx, cy) in char_size_list:
                count = count_child(hierarcy, index)
                if count == num_child:
                    return char
    return None

def check_sizemap():
    check_map = {}
    for _, (_, char_size_list) in size_of_charmap.items():
        for size,_,_ in char_size_list:
            global min_val, max_val
            if min_val > size:
                min_val = size
            if max_val < size:
                max_val = size
            if size in check_map:
                raise 'duplicatedd'
            check_map['size'] = size

check_sizemap()

im = cv2.imread('50048.png')
height, width, channel = im.shape
im2 = np.zeros((im.shape[0], im.shape[1], 3), np.uint8)
im3 = cv2.imread('50048.png')
#im2 = copy.deepcopy(im)

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im = None

ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )

offset_map = {
    '0': (0, 0),
    '1': (0, 40),
    '2': (0, 40 * 2),
    '3': (0, 40 * 3),
    '4': (0, 40 * 4),
    '5': (0, 40 * 5),
    '6': (0, 40 * 6),
    '7': (0, 40 * 7),
    '8': (0, 40 * 8),
    '9': (0, 40 * 9),
    'A': (0, 40 * 10),
    'B': (0, 40 * 11),
    'C': (0, 40 * 12),
    'D': (0, 40 * 13),
}

results = []

#輪郭描画
for i in range(len(contours)):
    contour = contours[i]
    area = cv2.contourArea(contour)
    x,y,w,h = cv2.boundingRect(contour)
    M = cv2.moments(np.subtract(contour, (x,y)))

    try:
        char = find_char(area, int(M['m10']/M['m00']), int(M['m01']/M['m00']), hierarchy, i)
        if char is None:
            continue
    except ZeroDivisionError:
        continue
    print("%s\t%d\tcx=%d\tcy=%d" % (char, area, int(M['m10']/M['m00']), int(M['m01']/M['m00'])))

    offset_x, offset_y = offset_map.get(char, 0)
    diff_x = x - offset_x
    diff_y = y - offset_y
    cv2.drawContours(im2, [np.subtract(contour, (diff_x, diff_y))], -1, (0,255,0), -1)
    offset_map[char] = (offset_x + 40, offset_y)
    cv2.drawContours(im3, [contour], -1, (0, 255, 0), -1)
    results.append(CharPos(char, x, y))

cv2.imwrite('resultA.png', im2)
cv2.imwrite('resultB.png', im3)

for i in range(len(results)):
    for j in range(i + 1, len(results)):
        if i == j:
            continue
        i_char = results[i]
        j_char = results[j]
if abs(i_char.y - j_char.y) < 5 and abs(i_char.x - j_char.x) < 35:
    if i_char.x < j_char.x:
        i_char.next = j_char
        j_char.prev = i_char
    if i_char.x > j_char.x:
        j_char.next = i_char
        i_char.prev = j_char

for result in results:
    if result.prev is not None:
        continue
    if result.next is not None:
        text = result.char
        while result.next is not None:
            result = result.next
            text += result.char
        print(text)

