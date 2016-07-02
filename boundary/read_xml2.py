# -*- coding: utf-8 -*-
import os
import re
from xml.etree import ElementTree

import sys

from common.db_connection_builder import DbConnectionBuilder

FEATURE_MEMBER = '{http://www.opengis.net/gml}featureMember'
KEN_NAME = '{http://www.safe.com/gml/fme}KEN_NAME'
GST_NAME = '{http://www.safe.com/gml/fme}GST_NAME'
CSS_NAME = '{http://www.safe.com/gml/fme}CSS_NAME'
MOJI = '{http://www.safe.com/gml/fme}MOJI'
X_CODE = '{http://www.safe.com/gml/fme}X_CODE'
Y_CODE = '{http://www.safe.com/gml/fme}Y_CODE'
POS_LIST = '{http://www.opengis.net/gml}posList'
EXTERIOR = '{http://www.opengis.net/gml}exterior'

dir_list = ['chiba', 'kanagawa', 'saitama', 'tokyo']


def xml_file_handler(connection, file):
    print("file " + file)
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.getchildren():
        if e.tag != FEATURE_MEMBER:
            continue
#        print("---------------")
        prefecture = None
        city_name1 = None
        city_name2 = None
        town_name = None
        boundary = None
        for e2 in e.getiterator():
            if e2.tag == KEN_NAME:
                prefecture = e2.text
            if e2.tag == GST_NAME:
                city_name1 = e2.text
                if city_name1 == ' ':
                    city_name1 = ''
            if e2.tag == CSS_NAME:
                city_name2 = e2.text
                if city_name2 == ' ':
                    city_name2 = ''
            if e2.tag == MOJI:
                town_name = e2.text
            if e2.tag == EXTERIOR:
                for e3 in e2.getiterator():
                    if e3.tag == POS_LIST:
                        if boundary is not None:
                            raise Exception()
                        boundary = e3.text
        print('%s %s%s %s %s' % (prefecture, city_name1, city_name2, town_name, boundary))
        name = "%s %s%s %s" % (prefecture, city_name1, city_name2, town_name)
        register_boundary2(connection, boundary, name)
        connection.commit()

#        print("ok %s %s %s" % (prefecture_id, city_id, town_id))
def register_boundary2(connection, boundary, name):
    sql = """
    INSERT INTO boundary2
        (boundary, name)
    VALUES(%s, %s);
    """
    cursor = connection.cursor()
    cursor.execute(sql, (boundary, name))
    return cursor.lastrowid

def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)

    for directory in dir_list:
        files = os.listdir(directory)
        files.sort()
        for file in files:
            xml_file_handler(connection, directory + os.sep + file)
    connection.close()


if __name__ == '__main__':
    main()