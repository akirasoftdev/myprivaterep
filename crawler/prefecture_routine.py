# -*- coding: utf-8 -*-
from common.db_cache.prefecture_cache import PrefectureCache


class PrefectureRoutine(object):
    PREFECTURES = [
        {
            'name': '東京都',
            'url': 'http://www.athome.co.jp/mansion/chuko/tokyo/city/',
            'area': ['//*[@id="00100"]', '//*[@id="00110"]', '//*[@id="00120"]']
        },
        {
            'name': '神奈川県',
            'url': 'http://www.athome.co.jp/mansion/chuko/kanagawa/city/',
            'area': ['//*[@id="00140"]', '//*[@id="00130"]', '//*[@id="00680"]', '//*[@id="00150"]']},
        {
            'name': '千葉県',
            'url': 'http://www.athome.co.jp/mansion/chuko/chiba/city/',
            'area': ['//*[@id="00160"]', '//*[@id="00170"]']
        },
        {
            'name': '埼玉県',
            'url': 'http://www.athome.co.jp/mansion/chuko/saitama/city/',
            'area': ['//*[@id="00180"]', '//*[@id="00190"]']
        }
    ]

    @classmethod
    def do(cls, context, callback):
        cursor = context.connection.cursor()
        prefecture_cache = PrefectureCache(cursor)

        for prefecture in cls.create_prefecture_list(context):
            context.set_prefecture(prefecture['name']).save()

            prefId = prefecture_cache.register(cursor, prefecture['name'])
            callback(context, prefId, prefecture['url'], prefecture['area'])

        context.set_prefecture(None).save()

    @classmethod
    def create_prefecture_list(cls, context):
        last_prefecture_proceed = context.get_prefecture()
        if last_prefecture_proceed is None:
            return cls.PREFECTURES
        for i in range(0, len(cls.PREFECTURES)):
            if cls.PREFECTURES[i]['name'] != last_prefecture_proceed:
                continue
            return cls.PREFECTURES[i:]
