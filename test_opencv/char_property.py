# -*- coding: utf-8 -*-


class CharProperty(object):
    def __init__(self, char, num_child, min_w, max_w, min_h, max_h, min_area, max_area, min_cx, max_cx, min_cy, max_cy):
        self.char = char
        self.num_child = num_child
        self.min_w = min_w
        self.max_w = max_w
        self.min_h = min_h
        self.max_h = max_h
        self.min_area = min_area
        self.max_area = max_area
        self.min_cx = min_cx
        self.max_cx = max_cx
        self.min_cy = min_cy
        self.max_cy = max_cy