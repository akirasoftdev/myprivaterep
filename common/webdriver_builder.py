# -*- coding: utf-8 -*-
from selenium import webdriver

class WebDriverBuilder(object):

    @classmethod
    def build(cls, path):
        return webdriver.Chrome(path)
