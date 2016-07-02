# -*- coding: utf-8 -*-
import os
import re
from xml.etree import ElementTree

import sys

from common.db.boundary_table import BoundaryTable
from common.db_cache.city_cache import CityCache
from common.db_cache.prefecture_cache import PrefectureCache
from common.db_cache.town_cache import TownCache
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

ABORT_ADDRESS_LIST = [
    ('千葉県','印旛郡栄町','新田'),
    ('千葉県', '印旛郡栄町', '安食田中，白山'),
    ('千葉県', '松戸市', '江戸川周辺水域（北部）'),
    ('千葉県', '松戸市', '江戸川周辺水域（南部）'),
    ('千葉県', '船橋市', '水面'),
    ('千葉県', '木更津市', '中島地先'),
    ('千葉県', '木更津市', '内港'),
    ('千葉県', '柏市', '上三ケ尾飛地'),
    ('千葉県', '柏市', '下三ケ尾飛地'),
    ('千葉県', '柏市', '西三ケ尾飛地'),
    ('千葉県', '市原市', '山之郷飛地'),
    ('千葉県', '香取市', '水郷団地'),
    ('千葉県', '香取市', '住金住宅団地'),
    ('千葉県', '長生郡長生村', '本郷、宮成'),
    ('神奈川県', '横浜市鶴見区', '公有水面調査区'),
    ('神奈川県', '横浜市神奈川区', '公有水面'),
    ('神奈川県', '横浜市磯子区', '水面'),
    ('神奈川県', '横浜市金沢区', '水面'),
    ('神奈川県', '川崎市川崎区', '水面'),
    ('埼玉県', '熊谷市', '利根川河川敷'),
    ('埼玉県', '東松山市', '市の川区画整理事業区域'),
    ('埼玉県', '戸田市', '堤外地'),
    ('埼玉県', '朝霞市', '（陸上自衛隊朝霞駐屯地）'),
    ('埼玉県', '三郷市', '江戸川河川敷'),
    ('埼玉県', '比企郡嵐山町', '平沢土地区画整理区域内'),
    ('東京都', '大田区', '羽田沖水面'),
    ('東京都', '大田区', '多摩川河川敷（上流）'),
    ('東京都', '大田区', '多摩川河川敷（下流）'),
    ('東京都', '調布市', '下布田'),
    ('東京都', '羽村市', '多摩川'),
    ('東京都', '西多摩郡瑞穂町', '横田基地'),
    ('東京都', '西多摩郡檜原村', '大嶽'),
    ('東京都', '新島村', '鵜渡根島'),
]

dir_list = ['chiba', 'kanagawa', 'saitama', 'tokyo']

def xml_file_handler(connection, prefecture_cache, city_cache, town_cache, file):
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
        x_code = None
        y_code = None
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
            if e2.tag == X_CODE:
                x_code = e2.text
            if e2.tag == Y_CODE:
                y_code = e2.text
        if town_name == ' ':
            continue
        print('%s %s%s %s %s' % (prefecture, city_name1, city_name2, town_name, boundary))
        if (prefecture, city_name1 + city_name2, town_name) in ABORT_ADDRESS_LIST:
            print("SKIP %s %s %s" % (prefecture, city_name1 + city_name2, town_name))
            continue
        prefecture_id = find_prefecture(prefecture_cache, prefecture)
        city_id = find_city_id(city_cache, city_name1 + city_name2, prefecture_id)
        town_id = find_town_id(connection, town_cache, town_name, city_id)

        BoundaryTable.register(connection.cursor(), town_id, x_code, y_code, boundary)
        connection.commit()

#        print("ok %s %s %s" % (prefecture_id, city_id, town_id))


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()

    prefecture_cache = PrefectureCache(cursor)
    city_cache = CityCache(cursor)
    town_cache = TownCache(connection.cursor())

    for directory in dir_list:
        files = os.listdir(directory)
        files.sort()
        for file in files:
            xml_file_handler(connection, prefecture_cache, city_cache, town_cache, directory + os.sep + file)
    connection.close()


def find_prefecture(prefecture_cache, prefecture):
    prefecture_id = prefecture_cache.get_by_name(prefecture)
    return prefecture_id


def find_city_id(city_cache, address, prefecture_id):
    for city in city_cache.get_all(prefecture_id):
        r = re.compile("^(%s).*" % (city['name']))
        m = r.search(address)
        if m is not None:
            return city['id']
    raise Exception(address)


def find_town_id(connection, town_cache, town_name, city_id):
    town2 = exclude_tails(town_name)
    town_rows = town_cache.get_by_names(town2, city_id)
    if len(town_rows) == 0:
        new_rows = test(connection, town_cache, town_name, city_id)
        if new_rows is not None:
            return new_rows['id']
        print('address = %s, town2 = %s' % (town_name, town2))
        raise
    return town_rows[0]['id']


def test(connection, town_cache, town_name, city_id):
    m = re.compile('大字(.*)').search(town_name)
    if m is None:
        return
    town_rows = town_cache.get_by_names(m.groups()[0], city_id)
    if len(town_rows) == 0:
        return
    town_id = town_rows[0]['id']
    town_cache.add_town_name(connection.cursor(), town_id, town_name)
    connection.commit()
    return {'id': town_id}


def exclude_city_name_from_address(self, address, city_rows):
    ret = ''
    for row in city_rows:
        city_name = row['name']
        r = re.compile('^%s(.*)$' % (city_name,))
        m = r.search(address)
        if m is None:
            continue
        address2 = m.group(1)
        if len(ret) > len(address2) or len(ret) == 0:
            ret = address2
    return ret


EXCLUDE_LIST = [
    u'(.+)[一二ニ三四五六七八九]丁目',
    u'(.*)（.*）[１-９]丁目',
    u'(.*)[１-９]{2}丁目',
    u'(.*)[１-９]丁目',
    u'(.*)（台）',
    u'(.*)（山之越）',
    u'(.*)（高谷）',
    u'(.*)（田代北）',
    u'(.*)（峯之越）',
    u'(.*)（.*）',
]


def exclude_tails(address):
    for pattern in EXCLUDE_LIST:
        m = re.compile(pattern).search(address)
        if m is not None:
            return m.group(1)
    r = re.compile(u'^([^０-９]+)')
    m = r.search(address)
    if m is not None:
        return m.group(1)
    return address

if __name__ == '__main__':
    main()