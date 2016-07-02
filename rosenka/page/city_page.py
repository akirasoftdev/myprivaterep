# -*- coding: utf-8 -*-


class Data(object):
    def __init__(self, name, id):
        self.town_name = name
        self.town_id = id


class CityPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.list = []

    def do(self):
        area_name_array = self.driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/table/tbody/tr[*]/th[2]')
        for area_name in area_name_array[1:]:
            links = area_name.find_elements_by_xpath('../td[*]/a')
            for link in links:
                self.list.append(Data(area_name.text, link.text))

    def get(self):
        return self.list