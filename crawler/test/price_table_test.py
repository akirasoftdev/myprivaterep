# -*- coding: utf-8 -*-
import unittest

from test.db_util import DbUtil

from common.db.price_table import PriceTable


class PriceTableTest(unittest.TestCase):
    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            PriceTable.clear_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            PriceTable.clear_all(cursor)
            num = PriceTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            id = PriceTable.register(cursor, 1, 100)

            # then:
            route = PriceTable.get(cursor, id)
            self.assertEqual(route, 100)

            cursor.close()
        self.connection.commit()

    def test_regsiterSucceedsTwice(self):
        with self.connection.cursor() as cursor:
            # given:
            PriceTable.register(cursor, 1, 100)

            # when:
            id_second = PriceTable.register(cursor, 1, 200)

            # then:
            name = PriceTable.get(cursor, id_second)
            self.assertEqual(name, 200)

            cursor.close()
        self.connection.commit()

    def test_updateLatestDateSucceeds(self):
        with self.connection.cursor() as cursor:
            PriceTable.register(cursor, 1, 100)
            self.connection.commit()
            date = PriceTable.get_latest_date(cursor, 1)
            PriceTable.register(cursor, 1, 100)
            self.connection.commit()
            date2 = PriceTable.get_latest_date(cursor, 1)
            self.assertGreater(date, date2)


if __name__ == '__main__':
    unittest.main()
