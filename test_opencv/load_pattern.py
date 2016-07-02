# -*- coding: utf-8 -*-
import os
import re

from test_opencv.pattern import Pattern


class LoadPattern(object):
    def __init__(self):
        self.patterns = {}
        BASE_DIR='../rosenka/work/'
        files_map = {}
        files_map['0'] = os.listdir(BASE_DIR + '0')
        files_map['1'] = os.listdir(BASE_DIR + '1')
        files_map['2'] = os.listdir(BASE_DIR + '2')
        files_map['3'] = os.listdir(BASE_DIR + '3')
        files_map['4'] = os.listdir(BASE_DIR + '4')
        files_map['5'] = os.listdir(BASE_DIR + '5')
        files_map['6'] = os.listdir(BASE_DIR + '6')
        files_map['7'] = os.listdir(BASE_DIR + '7')
        files_map['8'] = os.listdir(BASE_DIR + '8')
        files_map['9'] = os.listdir(BASE_DIR + '9')
        files_map['a'] = os.listdir(BASE_DIR + 'A')
        files_map['b'] = os.listdir(BASE_DIR + 'B')
        files_map['c'] = os.listdir(BASE_DIR + 'C')
        files_map['d'] = os.listdir(BASE_DIR + 'D')
        files_map['e'] = os.listdir(BASE_DIR + 'E')
        files_map['f'] = os.listdir(BASE_DIR + 'F')
        files_map['g'] = os.listdir(BASE_DIR + 'G')
        files_map['z'] = os.listdir(BASE_DIR + 'Z')
        for char, files in files_map.items():
            for file in files:
                w, h, area, cx, cy = re.compile(
                    '^(\d+)\-(\d+)_(\d+\.\d)_(\d+\.\d+)\-(\d+.\d+).*$').search(file).groups()
                key = Pattern.to_key(w, h, area, cx, cy)
                if key not in self.patterns:
                    self.patterns[key] = Pattern(char, w, h, area, cx, cy)

    def load(self):
        return self.patterns
