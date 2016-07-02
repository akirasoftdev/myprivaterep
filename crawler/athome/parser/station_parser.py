# -*- coding: utf-8 -*-
import re


class StationParser(object):
    patterns = [
        '(.*)/(.*線)',
        '(.*)/(.*エクスプレス)',
        '(.*)/(.*ライナー)',
        '(.*)/(.*ゆりかもめ)',
        '(.*)/(.*モノレール)',
        '(.*)/(ブルーライン)',
        '(.*)/(シーサイドライン)',
        '(.*)/(グリーンライン)',
        '(.*)/(.*鉄道)',
        '(.*)/(湘南新宿ライン.*)',
        '(.*)/(成田スカイアクセス)',
        '(.+)/(小湊鐵道)'
    ]

    @classmethod
    def parse(cls, text):
        r = re.compile('(.*)\s*(【バス】.*)')
        m = r.search(text)
        if m is not None:
            text = m.group(1)
            if len(text) == 0:
                return (None, None)

        for pattern in cls.patterns:
            r = re.compile(pattern)
            m = r.search(text)
            if m is not None:
                return (m.group(1), m.group(2))

        r = re.compile('(.*線)「*(.*)駅」*.*')
        m = r.search(text)
        if m is not None:
            return (m.group(2), m.group(1))

        r = re.compile('(.*線)「(.*)」')
        m = r.search(text)
        if m is not None:
            return (m.group(2), m.group(1))

        r = re.compile('(.*道路).*')
        m = r.search(text)
        if m is not None:
            return (None, None)

        r = re.compile('(.*ライン)「(.*)」駅.*')
        m = r.search(text)
        if m is not None:
            return (m.group(2), m.group(1))

        raise Exception(text)
