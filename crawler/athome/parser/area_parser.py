# -*- coding: utf-8 -*-
import re


class AreaParser(object):

    @classmethod
    def parse(cls, area_text):
        r = re.compile("(\d*\.\d*)m²$")
        m = r.search(area_text)
        if len(m.groups()) > 0:
            return int(float(m.group(1)) * 100)
        raise Exception(area_text)
