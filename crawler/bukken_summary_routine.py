# -*- coding: utf-8 -*-
from athome.bukken_page import BukkenPage


class BukkenSummaryRoutine(object):

    @classmethod
    def do(cls, context, prefecutre_id):
        bukken = BukkenPage(context.driver, context.connection, prefecutre_id)

        page = 1
        last_summary_page_proceed = context.get_page()
        if last_summary_page_proceed is not None:
            page = int(last_summary_page_proceed)
            bukken.page_skip(last_summary_page_proceed)

        has_next = True
        while has_next:
            context.set_page(page).save()
            has_next = bukken.parse(context)
            page += 1

        context.set_page(None).save()
