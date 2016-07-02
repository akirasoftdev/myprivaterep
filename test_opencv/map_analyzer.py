# -*- coding: utf-8 -*-
import cv2

from test_opencv.load_pattern import LoadPattern
from test_opencv.pattern import Pattern


class MapAnalyzer(object):

    def __init__(self):
        self.min_area = 100
        self.max_area = 500
        self.min_cx = 4
        self.max_cx = 9
        self.min_cy = 10
        self.max_cy = 15
        self.min_h = 27
        self.max_h = 29
        self.min_w = 8
        self.max_w = 17
        self.patterns = LoadPattern().load()
        self.analysis = []

    def analyze(self, file_name):
        im = cv2.imread(file_name)

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours)):
            contour = contours[i]
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if w < self.min_w or w > self.max_w:
                continue
            if h < self.min_h or h > self.max_h:
                continue
            if area < self.min_area or area > self.max_area:
                continue

            (cx, cy) = self.get_center_pos(contour)
            (child_count, area2) = self.count_child(contours, hierarchy, i)

            key = Pattern.to_key_child(w, h, area2, cx, cy, child_count)
            if key in self.patterns:
                self.analysis.append({'x':x, 'y':y, 'pattern':self.patterns[key]})
        return self.analysis

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
