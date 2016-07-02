# -*- coding: utf-8 -*-
from athome.parser.prefecture_page import PrefecturePage


class MaroriRoutine(object):

    @classmethod
    def do(cls, context, prefecture_id, url, area_xpaths, callback):
        last_marodi_proceed = context.get_madori()
        if last_marodi_proceed is None:
            last_marodi_proceed = 1

        for madoriIndex in range(last_marodi_proceed, 13):
            context.set_madori(madoriIndex).save()
            PrefecturePage.check_param_and_open_summay(url, context.driver, madoriIndex, area_xpaths)
            callback(context, prefecture_id)

        context.set_madori(None).save()
