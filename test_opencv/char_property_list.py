# -*- coding: utf-8 -*-
from test_opencv.char_property import CharProperty

char_properties = [
    CharProperty('0', 1, 13, 17, 27, 29, 238.0, 371.0, 6.254, 7.919, 12.512, 14.521),
    CharProperty('1', 0,  8, 13, 27, 29, 105.5, 156.5, 4.758, 8.667, 11.122, 13.732),
    CharProperty('2', 0, 15, 17, 27, 29, 175.5, 231.0, 6.901, 8.873, 12.795, 14.989),
    CharProperty('3', 0, 11, 17, 27, 29, 146.5, 222.0, 5.753, 9.584, 12.931, 14.546),
    CharProperty('4', 1, 17, 17, 27, 29, 209.0, 245.5, 8.394, 8.678, 13.099, 14.763),
    CharProperty('5', 0, 15, 17, 27, 29, 203.0, 250.0, 6.494, 8.387, 12.313, 13.970),
    CharProperty('6', 1, 15, 15, 27, 29, 261.0, 303.5, 6.834, 7.036, 13.571, 15.181),
    CharProperty('7', 0, 15, 15, 27, 29, 129.5, 168.0, 7.842, 8.133,  9.916, 11.308),
    CharProperty('8', 2, 15, 17, 27, 29, 303.0, 345.0, 6.908, 7.911, 12.923, 14.452),
    CharProperty('9', 1,  8, 17, 27, 29, 132.0, 308.5, 2.780, 8.876, 11.724, 14.491),
    CharProperty('A', 1,  8, 17, 27, 29, 105.0, 450.0, 4.5,  10.0,    9.5,   15.5),
    CharProperty('B', 2, 17, 17, 27, 29, 370.5, 402.5, 7.187, 7.304, 13.004, 14.182),
    CharProperty('C', 0, 17, 17, 27, 29, 185.5, 237.0, 7.443, 7.789, 12.939, 14.333),
    CharProperty('D', 1, 16, 17, 27, 29, 335.5, 401.0, 6.583, 7.388, 12.712, 14.148),
    CharProperty('E', 0, 16, 16, 27, 29, 209.0, 248.0, 5.461, 5.900, 12.619, 14.494),
    CharProperty('F', 0, 16, 16, 27, 29, 165.5, 195.5, 4.466, 4.982, 10.087, 11.183),
    CharProperty('G', 1,  8, 17, 27, 29, 105.0, 450.0, 4.5,  10.0,    9.5,   15.5),
]


def find_char_property(num_child, w, h, area, cx, cy):
    for p in char_properties:
        if num_child != p.num_child:
            continue
        if w < p.min_w or w > p.max_w:
            continue
        if h < p.min_h or h > p.max_h:
            continue
        if area < p.min_area or area > p.max_area:
            continue
        if cx < p.min_cx or cx > p.max_cx:
            continue
        if cy < p.min_cy and cy > p.max_cy:
            continue
        return p.char
    return None
