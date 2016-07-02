# -*- coding: utf-8 -*-


class Pattern(object):
    def __init__(self, char, w, h, area, cx, cy):
        self.char = char
        self.w = w
        self.h = h
        self.area = area
        self.cx = cx
        self.cy = cy

    @classmethod
    def to_key(cls, w, h, area, cx, cy):
        return '%s-%s_%.1f_%.3f-%.3f' % (w, h, float(area), float(cx), float(cy))

    @classmethod
    def to_key_child(cls, w, h, area, cx, cy, child):
        return '%d-%d_%.1f_%.3f-%.3f_%d' % (w, h, area, cx, cy, child)

    def __str__(self):
        return 'pattern: (%s)%s-%s_%s_%s-%s' % (self.char, self.w, self.h, self.area, self.cx, self.cy)