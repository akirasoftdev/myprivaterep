# -*- coding: utf-8 -*-
import os
import re
import sys
import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from crawler.athome.adjust_station_name import AdjustStationName

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from crawler.athome.parser.area_parser import AreaParser
from crawler.athome.parser.floor_parser import FloorParser
from crawler.athome.parser.year_parser import YearParser
from crawler.athome.parser.structure_parser import StructureParser
from crawler.athome.parser.layout_parser import LayoutParser
from crawler.athome.parser.page_num_parser import PageNumParser
from crawler.athome.parser.station_parser import StationParser
from crawler.athome.parser.time_parser import TimeParser
from crawler.athome.validate_bukken import ValidateBukken
from common.db.bukken_table import BukkenTable
from common.db_cache.city_cache import CityCache
from common.db_cache.town_cache import TownCache
from common.db_cache.station_cache import StationCache


class BukkenPage(object):

    def __init__(self, driver, connection, prefecture_id):
        self.driver = driver
        self.connection = connection
        self.prefecture_id = prefecture_id
        self.city_cache = CityCache(connection.cursor())
        self.town_cache = TownCache(connection.cursor())
        self.station_cache = StationCache(connection.cursor())

    def skip(self, target_page):
        result = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[1]/div[2]/ul/li[*]/a')

        result.reverse()
        for link in result:
            if '最初へ' in link.text:
                continue
            if '前へ' in link.text:
                continue
            if '次へ' in link.text:
                continue
            if '最後へ' in link.text:
                continue

            page_num = int(link.text)
            if page_num == target_page:
                link.click()
                return
            if page_num < target_page:
                link.click()
                return
        raise Exception()

    def wait_loading(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="loading"]'))
            )
        except TimeoutException:
            raise Exception("page check Timeout Error")

    def get_current_page(self):
        page_num_text = self.driver.find_element_by_xpath('//*[@id="listPage-header"]/h1').text
        return PageNumParser.parse(page_num_text)

    def page_skip(self, skip_page):
        self.wait_loading()

        while skip_page != self.get_current_page():
            self.skip(int(skip_page))
            self.wait_loading()

    def parse(self, context):
        print("parse")
        self.wait_loading()
        page_num_text = self.driver.find_element_by_xpath('//*[@id="listPage-header"]/h1').text
        context.set_page(PageNumParser.parse(page_num_text))
        context.save()

        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="item-list"]/div[2]/p[1]/label/a'))
            )
            # URLおよびタイトル
            bukken_urls = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/p[1]/label/a')
            num_of_bukken = len(bukken_urls)

            # 価格
            price_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[3]/span/span')
            if len(price_array) != num_of_bukken:
                raise Exception('unexpected')

            # 住所
            address_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[1]/div[2]/span')
            if len(address_array) != num_of_bukken:
                raise Exception('unexpected')

            # 間取
            layout_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[5]/span[1]')
            if len(layout_array) != num_of_bukken:
                raise Exception('unexpected')

            #築年数
            year_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[6]/span[2]')
            if len(year_array) != num_of_bukken:
                raise Exception('unexpected')

            # 専有面積
            occupied_area_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[5]/span[2]')
            if len(occupied_area_array) != num_of_bukken:
                raise Exception('unexpected')

            # 階数
            floors_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[4]/span[2]')
            if len(floors_array) != num_of_bukken:
                raise Exception('unexpected')

            # 構造
            structure_array = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[4]/span[1]')
            if len(structure_array) != num_of_bukken:
                raise Exception('unexpected')

            # 最寄り駅
            time_for_station = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[2]')
            if len(time_for_station) != num_of_bukken:
                raise Exception('unexpected')

            stations = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[*]/div/div[2]/ul/li[1]/div[1]/span')
            if len(stations) != num_of_bukken:
                raise Exception('unexpected')

            for i in range(len(bukken_urls)):
                with self.connection.cursor() as cursor:
                    params = {'cursor': cursor,}
                    params['url'] = bukken_urls[i].get_attribute('href')
                    params['title'] = bukken_urls[i].text
                    params['address'] = address_array[i].text
                    params['prefecture_id'] = self.prefecture_id
                    try:
                        params['city_id'] = self.find_city_id(params['address'], self.prefecture_id)
                        params['town_id'] = self.find_town_id(params['address'], params['city_id'])
                    except Exception as e:
                        print(e)
                        continue
                    floors = FloorParser.parse(floors_array[i].text)
                    params['building_floors'] = floors[0]
                    params['under_ground'] = floors[1]
                    params['room_floor'] = floors[2]
                    params['occupied_area'] = AreaParser.parse(occupied_area_array[i].text)
                    price = price_array[i].text.replace(",", "")
                    price = price.split('.')[0]
                    params['price'] = int(price)
                    params['layout'] = LayoutParser.parse(layout_array[i].text)
                    params['year'] = YearParser.parse(year_array[i].text)
                    params['structure'] = StructureParser.parse(structure_array[i].text)
                    station, line = StationParser.parse(stations[i].text)
                    if station is None or line is None:
                        print("station : %s" % stations[i].text)
                        print("skip this bukken because of station unknown")
                        continue
                    station, line = AdjustStationName.do(station, line)
                    params['station_id'] = self.station_cache.get(cursor, station, line)
                    if params['station_id'] is None:
                        print("station : %s , %s" % (station, line))
                        print("skip this bukken because of station unknown#2")
                        continue

                    walk_time = TimeParser.parse(time_for_station[i].text)
                    if walk_time == -1 or walk_time > 30:
                        walk_time = 30
                    params['walk_time'] = walk_time
                    params['last_modified'] = datetime.date.today()

                    if not ValidateBukken.validate(**params):
                        print("skip this bukken")
                        continue

                    try:
                        BukkenTable.register(**params)
                        self.connection.commit()
                    except Exception as e:
                        if e.args[0] == 1062:
                            print(e)
                        else:
                            print(e)
                            raise


            items = self.driver.find_elements_by_xpath('//*[@id="item-list"]/div[1]/div[2]/ul/li[*]/a[1]')
            for item in items:
                if item.text == '次へ' :
                    item.click()
                    return True
            return False
        except TimeoutException:
            print("Timeout Error")
        return False

    def find_city_id(self, address, prefecture_id):
        for city in self.city_cache.get_all(prefecture_id):
            r = re.compile("^(%s).*" % (city['name']))
            m = r.search(address)
            if m is not None:
                return city['id']
        raise Exception(address)

    def find_town_id(self, address, city_id):
        city_rows = self.city_cache.get_by_id(city_id)
        town_adddress = self.exclude_city_name_from_address(address, city_rows)
        town2 = self.exclude_tails(town_adddress)
        town_rows = self.town_cache.get_by_names(town2, city_id)
        if len(town_rows) == 0:
            print('address = %s, town2 = %s' %(address, town2))
            raise
        return town_rows[0]['id']

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

    def exclude_tails(self, address):
        r = re.compile(u'^([^０-９]*)')
        m = r.search(address)
        if m is not None:
            return m.group(1)
        return address
