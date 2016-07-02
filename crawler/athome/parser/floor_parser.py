# -*- coding: utf-8 -*-
import re


class FloorParser(object):

    @classmethod
    def parse(cls, floor_text):
        r = re.compile("地上(\d*)階地下(\d*)階建\s/\s.*(\d)階部分")
        m = r.search(floor_text)
        if m is not None:
            return (m.group(1), m.group(2), m.group(3))

        r = re.compile("(\d*)階建\s/\s.*(\d)階部分")
        m = r.search(floor_text)
        if m is not None:
            return (m.group(1), 0, m.group(2))

        r = re.compile("地上(\d*)階地下(\d*)階建\s/\s(\d*)階$")
        m = r.search(floor_text)
        if m is not None:
            return (m.group(1), m.group(2), m.group(3))

        r = re.compile("地上(\d*)階地下(\d*)階建\s/\s地下(\d*)階$")
        m = r.search(floor_text)
        if m is not None:
            return (m.group(1), m.group(2), str(int(m.group(3)) * -1))

        r = re.compile("(\d*)階建\s/\s(\d*)階$")
        m = r.search(floor_text)
        if m is not None:
            return (m.group(1), 0, m.group(2))

        r = re.compile("(\d*)階建$")
        m = r.search(floor_text)
        if m is not None:
            return (m.group(1), 0, 0)

        raise Exception(floor_text)
