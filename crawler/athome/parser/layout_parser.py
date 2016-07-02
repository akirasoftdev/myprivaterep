# -*- coding: utf-8 -*-


class LayoutParser(object):

    layout_map = {
        'ワンルーム':'1R',
        '1K':'1K','2K':'2K','3K':'3K','4K':'4K','5K':'5K',
        '1SK':'1SK','2SK':'2SK','3SK':'3SK','4SK':'4SK','5SK':'5SK',
        '1DK':'1DK','2DK':'2DK','3DK':'3DK','4DK':'4DK','5DK':'5DK',
        '1LK':'1LK','2LK':'2LK','3LK':'3LK','4LK':'4LK','5LK':'5LK',
        '1SDK':'1SDK','2SDK':'2SDK','3SDK':'3SDK','4SDK':'4SDK','5SDK':'5SDK',
        '1SLK':'1SLK','2SLK':'2SLK','3SLK':'3SLK','4SLK':'4SLK','5SLK':'5SLK',
        '1LDK':'1LDK','2LDK':'2LDK','3LDK':'3LDK','4LDK':'4LDK','5LDK':'5LDK',
        '1SLDK':'1SLDK','2SLDK':'2SLDK','3SLDK':'3SLDK','4SLDK':'4SLDK','5SLDK':'5SLDK'
    };

    @classmethod
    def parse(cls, layout_text):
        return cls.layout_map[layout_text]
