#coding:utf-8
import numpy as np
import cv2

from test_opencv.char_property_list import find_char_property
from test_opencv.load_pattern import LoadPattern
from test_opencv.pattern import Pattern
patterns = LoadPattern().load()

class CharPos(object):
    def __init__(self, char, x, y, w, h):
        self.char = char
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.next = None
        self.prev = None

size_of_charmap = {
    '0': (1, [(351.5, 7, 13), (357.5, 7, 13), (358.5, 7, 13), (359.5, 7, 13), (379.5, 8, 13), (380.5, 8, 13),
              (381.5, 8, 13), (385.5, 8, 13), (386.5, 8, 13)]),
    '1': (0, [(118.5, 5, 13), (119.5, 5, 13), (122.5, 6, 13), (122.5, 5, 13), (123.5, 6, 13), (123.5, 5, 13),
              (145.5, 6, 13)]),
    '2': (0, [(193.5, 6, 14), (193.5, 7, 14), (194.5, 7, 14), (197.5, 7, 14), (200.5, 7, 14), (207.5, 7, 14),
              (208.5, 7, 14), (209.5, 7, 14), (210.5, 7, 14), (212.5, 7, 14), (213.5, 7, 14), (217.5, 7, 14)]),
    '3': (0, []),
    '4': (1, [(237.0, 9, 14)]),
    '5': (0, [(219.0, 7, 13), (223.0, 7, 13), (224.0, 7, 13), (227.0, 7, 13), (230.0, 7, 13), (236.0, 8, 13),
              (236.0, 7, 13), (239.0, 8, 13), (241.0, 7, 13)]),
    '6': (1, [(301.0, 7, 15), (312.0, 7, 15)]),
    '7': (0, [(147.5, 7, 10), (164.5, 8, 11)]),
    '8': (2, [(329.0, 7, 14), (332.0, 7, 14), (353.0, 8, 14), (356.0, 8, 14), (357.0, 8, 14)]),
    '9': (1, []),
    'A': (1, []),
    'B': (2, []),
    'C': (0, []),
    'D': (1, [(362.5, 6, 13), (363.5, 6, 13), (364.5, 6, 13), (365.5, 6, 13), (385.5, 7, 13), (386.5, 7, 13),
              (388.5, 7, 13), (390.5, 7, 13), (392.5, 7, 13), (393.5, 7, 13)]),
}

min_val = 99999
max_val = 0

def count_child(hierarcy, index):
    count = 0
    next,_,child,_ = hierarcy[0][index]
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
    if size < min_val or size > max_val:
        return None
    for char, (num_child, char_size_list) in size_of_charmap.items():
        if (size, cx, cy) in char_size_list:
            count = count_child(hierarcy, index)
            if count == num_child:
                return char

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

class Reader(object):

    def __init__(self, img_path):
        self.img_path = img_path
        im = cv2.imread(img_path)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        char_pos_list = []
        for i in range(len(contours)):
            contour = contours[i]
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = self.get_center_pos(np.subtract(contour, (x, y)))
            if cx is None or cy is None:
                continue
            key = Pattern.to_key(w, h, area, cx, cy)
            if key not in patterns:
                continue
            char = patterns[key].char
            print(char)
            char_pos_list.append(CharPos(char, x, y, w, h))

        for i in range(len(char_pos_list)):
            for j in range(i + 1, len(char_pos_list)):
                if i == j:
                    continue
                i_char = char_pos_list[i]
                j_char = char_pos_list[j]
                if abs(i_char.y - j_char.y) < 5 and abs(i_char.x - j_char.x) < 35:
                    if i_char.x < j_char.x:
                        i_char.next = j_char
                        j_char.prev = i_char
                    if i_char.x > j_char.x:
                        j_char.next = i_char
                        i_char.prev = j_char

        self.results = []
        for char_pos in char_pos_list:
            if char_pos.prev is not None:
                continue
            if char_pos.next is not None:
                text = char_pos.char
                pos_x1 = char_pos.x
                pos_y1 = char_pos.y
                pos_x2 = char_pos.x + char_pos.w
                pos_y2 = char_pos.y + char_pos.h
                while char_pos.next is not None:
                    char_pos = char_pos.next
                    text += char_pos.char
                    pos_y1 = pos_y1 if pos_y1 < char_pos.y else char_pos.y
                    pos_x2 = char_pos.x + char_pos.w
                    pos_y2 = pos_y2 if pos_y2 > char_pos.y + char_pos.h else char_pos.y + char_pos.h

                self.results.append((text, pos_x1, pos_y1, pos_x2 - pos_x1, pos_y2 - pos_y1))

    def get_center_pos(self, contour):
        M = cv2.moments(contour)
        if M['m10'] == 0.0 or M['m01'] == 0.0:
            return (None, None)

        cx = M['m10'] / M['m00']
        cy = M['m01'] / M['m00']
        return (cx, cy)

    def count_child(self, contours, hierarcy, index):
        count = 0
        area = cv2.contourArea(contours[index])
        next, _, child, _ = hierarcy[0][index]
        if child == -1:
            return (0, area)
        next = child
        while next != -1:
            area -= cv2.contourArea(contours[next])
            next, _, child, _ = hierarcy[0][next]
            if child != -1:
                return (0, None)
            count += 1
        return (count, area)

    def aaaa(self, img_path):
        self.img_path = img_path
        check_sizemap()
        im = cv2.imread(img_path)
        im2 = cv2.imread(img_path)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )
        char_pos_list = []

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
            char_pos_list.append(CharPos(char, x, y, w, h))
            cv2.drawContours(im2, [contour], -1, (0, 255, 0), -1)
        cv2.imwrite(img_path.replace('.png', '_tmp.png'), im2)

        for i in range(len(char_pos_list)):
            for j in range(i + 1, len(char_pos_list)):
                if i == j:
                    continue
                i_char = char_pos_list[i]
                j_char = char_pos_list[j]
                if abs(i_char.y - j_char.y) < 5 and abs(i_char.x - j_char.x) < 35:
                    if i_char.x < j_char.x:
                        i_char.next = j_char
                        j_char.prev = i_char
                    if i_char.x > j_char.x:
                        j_char.next = i_char
                        i_char.prev = j_char

        self.results = []
        for char_pos in char_pos_list:
            if char_pos.prev is not None:
                continue
            if char_pos.next is not None:
                text = char_pos.char
                pos_x1 = char_pos.x
                pos_y1 = char_pos.y
                pos_x2 = char_pos.x + char_pos.w
                pos_y2 = char_pos.y + char_pos.h
                while char_pos.next is not None:
                    char_pos = char_pos.next
                    text += char_pos.char
                    pos_y1 = pos_y1 if pos_y1 < char_pos.y else char_pos.y
                    pos_x2 = char_pos.x + char_pos.w
                    pos_y2 = pos_y2 if pos_y2 > char_pos.y + char_pos.h else char_pos.y + char_pos.h

                self.results.append((text, pos_x1, pos_y1, pos_x2 - pos_x1, pos_y2 - pos_y1))

    def get(self):
        return self.results