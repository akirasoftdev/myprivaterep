# -*- coding: utf-8 -*-
import re


class TimeParser(object):

    @classmethod
    def parse(cls, time_text):
        r = re.compile('(\d*)分')
        m = r.search(time_text)
        if m is not None:
            return int(m.group(1))
        if time_text == '－':
            return -1
        r = re.compile('(\d*)ｍ')
        m = r.search(time_text)
        if m is not None:
            return int(int(m.group(1)) / 80)
        raise Exception(time_text)
