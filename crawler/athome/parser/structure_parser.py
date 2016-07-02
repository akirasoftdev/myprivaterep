# -*- coding: utf-8 -*-


class StructureParser(object):
    structureMap = {
        'ＲＣ':'RC',
        'ＳＲＣ':'SRC',
        'ＳＲＣ造など':'SRC',
        '鉄骨造':'鉄骨造',
        '－':'－',
        'ＳＲＣ・ＲＣ':'SRC・RC',
        'ＰＣ':'PC',
        'ＡＬＣ':'ALC',
        'RC造一部SRC造':'RC',
        'ＲＣ・Ｓ陸屋根造':'RC',
        'ＲＣ造一部鉄骨造':'RC',
        '軽量鉄骨造':'軽量鉄骨造',
        'スチール':'スチール'
    }

    @classmethod
    def parse(cls, structure_text):
        try:
            return cls.structureMap[structure_text]
        except:
            print('構造 %s' % structure_text)
            return structure_text
