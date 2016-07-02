# -*- coding: utf-8 -*-
import unittest

from common.db.access_table import AccessTable


class AccessTableTest(unittest.TestCase):

    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            AccessTable.clear_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            AccessTable.clear_all(cursor)
            num = AccessTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            rid = AccessTable.register(cursor, 1, 2, 3, 4)

            # then:
            route = AccessTable.get(cursor, rid)
            self.assertEqual(route, 1)

            cursor.close()
        self.connection.commit()

    def test_register_succeeds_twice(self):
        with self.connection.cursor() as cursor:
            # given:
            AccessTable.register(cursor, 1, 2, 3, 4)

            # when:
            id_second = AccessTable.register(cursor, 11, 12, 13, 14)

            # then:
            name = AccessTable.get(cursor, id_second)
            self.assertEqual(name, 11)

            cursor.close()
        self.connection.commit()

if __name__ == '__main__':
    unittest.main()
