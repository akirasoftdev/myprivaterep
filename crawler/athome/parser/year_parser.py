# -*- coding: utf-8 -*-
import datetime
import re


class YearParser(object):

    @classmethod
    def parse(cls, year_text):
        r = re.compile("(\d*)年(\d*)月.*")
        m = r.search(year_text)
        if m is not None:
            year_ant_month = '' + m.group(1) + '-' + m.group(2)
            return datetime.datetime.strptime(year_ant_month, '%Y-%m')
        raise Exception(year_text)
