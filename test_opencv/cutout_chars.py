# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os

from test_opencv.char_property import CharProperty
from test_opencv.char_property_list import char_properties, find_char_property
from test_opencv.load_pattern import LoadPattern
from test_opencv.pattern import Pattern

min_area = 105.0
max_area = 450.0
min_cx = 4.5
max_cx = 10.0
min_cy = 9.5
max_cy = 15.5
min_h = 27
max_h = 29
min_w = 8
max_w = 19
min_area_d = [105.0, 130.0, 300]
max_area_d = [260.0, 450.0, 450.0]

patterns = LoadPattern().load()


class CutOutChars(object):

    def bbbbb(self, file_name):
        im = cv2.imread(file_name)
        im2 = cv2.imread(file_name)

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )
        for i in range(len(contours)):
            contour = contours[i]
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = self.get_center_pos(np.subtract(contour, (x, y)))
            child_count, area2 = self.count_child(contours, hierarchy, i)
            char = find_char_property(child_count, w, h, area, cx, cy)
            if char is None:
                continue
            color = (0, 255, 0)
            cv2.drawContours(im2, [contour], -1, color, -1)
        cv2.imwrite(file_name.replace('.png', '(tmp).png'), im2)


    def __init__(self, file_name):
        im = cv2.imread(file_name)
        im2 = cv2.imread(file_name)

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )
        for i in range(len(contours)):
            contour = contours[i]
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if y < 400:
                continue
            if w < min_w or w > max_w:
                continue
            if h < min_h or h > max_h:
                continue
            if area < min_area or area > max_area:
                continue

            cx, cy = self.get_center_pos(np.subtract(contour, (x, y)))
            if cx is None and cy is None:
                continue
            if cx < min_cx or cx > max_cx or cy < min_cy and cy > max_cy:
                cv2.drawContours(im2, [contour], -1, (255, 255, 0), -1)

            child_count, area2 = self.count_child(contours, hierarchy, i)
            if child_count > 2:
                continue
            if area < min_area_d[child_count] or area > max_area_d[child_count]:
                continue

            key = Pattern.to_key(w, h, area, cx, cy)
            color = (0, 255, 0)
            if key not in patterns:
                im3 = np.zeros((max_h, max_w, 3), np.uint8)
                cv2.drawContours(im3, [np.subtract(contour, (x, y))], -1, color, -1)
                filename = "%d-%d_%.1f_%.3f-%.3f.png" % (w, h, area, cx, cy)
                cv2.imwrite('test/%d/%s' % (child_count, filename), im3)
                color = (0, 0, 255)
            else:
                pattern = patterns[key]
                if pattern.char == 'z':
                    color = (0, 255, 255)
            cv2.drawContours(im2, [contour], -1, color, -1)

        cv2.imwrite(file_name.replace('.png', '(tmp).png'), im2)

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


if __name__ == '__main__':
    CutOutChars('work/50064.png')