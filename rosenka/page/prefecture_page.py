# -*- coding: utf-8 -*-

from page.city_page import CityPage

class Data(object):
    def __init__(self, city_name, town_name, town_id):
        self.city_name = city_name
        self.town_name = town_name
        self.town_id = town_id

class PrefecturePage(object):

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.list = []

    def do(self):
        self.driver.get(self.url)

        links_array = self.driver.find_elements_by_xpath('//*[@id="contents"]/table[2]/tbody/tr[*]/td[*]/a')
        href_list = [(link.text, link.get_attribute('href')) for link in links_array]
        for href in href_list:
            city_name = href[0]
            link = href[1]
            self.driver.get(link)
            city_page = CityPage(self.driver)
            city_page.do()
            town_data_list = city_page.get()
            for town_data in town_data_list:
                self.list.append(Data(city_name, town_data.town_name, town_data.town_id))

    def get(self):
        return self.list