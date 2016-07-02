# -*- coding: utf-8 -*-
import consts
from common.db.rosen_price_table import RosenPriceTable
from common.db_connection_builder import DbConnectionBuilder
import logging
LOG = logging.getLogger(__file__)
LOG.info('START')


class Rosenka:

    def __init__(self):
        self.rosen_price_map = {}
        conn = DbConnectionBuilder.build(consts.HOST_NAME, consts.PORT_NO)
        try:
            cursor = conn.cursor()
            rows = RosenPriceTable.getAll(cursor)
            for row in rows:
                self.rosen_price_map[row['townId']] = row['price']
        finally:
            conn.close()

    def get(self, town_id):
        if town_id not in self.rosen_price_map:
            return None
        return self.rosen_price_map[town_id]
