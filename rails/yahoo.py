# -*- coding: utf-8 -*-
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.db.transit_time_table import TransitTimeTable

URL='http://transit.yahoo.co.jp/?c=0'


class YahooTransit:
    def __init__(self, driver):
        self._driver = driver

    def run(self, stations, exclude_patterns, connection):
        cursor = connection.cursor()
        for i, src in enumerate(stations):
            for dst in stations[i:]:
                if src['name'] == dst['name']:
                    continue
                if (src['id'], dst['id'])  in exclude_patterns:
                    continue
                print(src['name'] + ":" + dst['name'])
                self._driver.get(URL)
                self._input_departure(src['name'])
                self._input_arrival(dst['name'])
                self._input_time()
                self._click_submit()
                try:
                    if not self._read_station(src['id'], dst['id']):
                        raise Exception()
                    transit_time = self._read_transit_time()
                    TransitTimeTable.register(cursor, src['id'], dst['id'], transit_time)
                    connection.commit()
                except:
                    pass

    def _input_departure(self, station_name):
        sfrom = self._driver.find_element_by_xpath('//*[@id="sfrom"]')
        sfrom.send_keys(station_name)

    def _input_arrival(self, station_name):
        sfrom = self._driver.find_element_by_xpath('//*[@id="sto"]')
        sfrom.send_keys(station_name)

    def _input_time(self):
        e = self._driver.find_element_by_xpath('//*[@id="y"]')
        e.send_keys('2016')
        e = self._driver.find_element_by_xpath('//*[@id="m"]')
        e.send_keys('10')
        e = self._driver.find_element_by_xpath('//*[@id="d"]')
        e.send_keys('21')
        e = self._driver.find_element_by_xpath('//*[@id="hh"]')
        e.send_keys('9')
        e = self._driver.find_element_by_xpath('//*[@id="mm"]')
        e.send_keys('0')
        pass

    def _click_submit(self):
        sfrom = self._driver.find_element_by_xpath('//*[@id="searchModuleSubmit"]')
        sfrom.submit()

    def _read_station(self, src_id, dst_id):
        xpath = '//*[@id="route01"]/div[4]/div[*]/dl/dt/a'
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        result = self._driver.find_elements_by_xpath(xpath)
        pattern = '.*/top/(\d+)/.*'
        first_id = re.compile(pattern).search(result[0].get_attribute('href')).group(1)
        last_id = re.compile(pattern).search(result[-1].get_attribute('href')).group(1)
        print("%s - %s, %s - %s" % (src_id, first_id, dst_id, last_id))
        return first_id == str(src_id) and last_id == str(dst_id)

    def _read_transit_time(self):
        xpath = '//*[@id="rsltlst"]/li[1]/dl/dd/ul/li[1]'
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        result = self._driver.find_element_by_xpath(xpath)
        # result.text : 10:48発→11:17着（29分）
        transit_time = re.compile('^.*（(.*)）$').search(result.text).group(1)

        # transit_time: 29分 or 1時間6分
        m = re.compile('(\d+)時間(\d+)分').search(transit_time)
        if m is not None:
            return self.to_minutes(int(m.group(1)), int(m.group(2)))
        m = re.compile('(\d+)分').search(transit_time)
        if m is not None:
            return int(m.group(1))
        raise Exception(transit_time)

    @staticmethod
    def to_minutes(hours, minutes):
        return hours * 60 + minutes

    def _read_line(self):
        xpath = '//*[@id="route01"]/div[4]/div[2]/div/ul/li[1]/div/text()'
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        result = self._driver.find_element_by_xpath(xpath)

