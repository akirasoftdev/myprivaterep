# -*- coding: utf-8 -*-
import re


class PageNumParser(object):

    @classmethod
    def parse(cls, text):
        r = re.compile("\s(\d*)ページ目")
        m = r.search(text)
        if m is not None:
            return int(m.group(1))
        return 1;

    def linkParse(self, text):
        return int(text)

