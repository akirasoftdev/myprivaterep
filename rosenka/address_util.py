# -*- coding: utf-8 -*-
import re


def cut_tail_num(town):
    r = re.compile(u'^([^０-９～]*)[０-９～]+')
    m = r.search(town)
    if m is not None:
        return m.group(1)

    r = re.compile(u'^([^（]*)（.*$')
    m = r.search(town)
    if m is not None:
        return m.group(1)

    r = re.compile(u'^([^イロハホ]+)[イロハホ]$')
    m = r.search(town)
    if m is not None:
        return m.group(1)

    r = re.compile(u'^([^0-9]*)[0-9]+')
    m = r.search(town)
    if m is not None:
        return m.group(1)

    return town
