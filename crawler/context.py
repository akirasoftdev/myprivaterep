# -*- coding: utf-8 -*-
import json


class Context(object):

    def __init__(self):
        self.condition = Context.get_initial_condition()
        self.driver = None
        self.connection = None

    def set_prefecture(self, prefecture):
        self.condition['prefecture'] = prefecture
        return self

    def get_prefecture(self):
        return self.condition.get('prefecture')

    def set_madori(self, madori):
        self.condition['madori'] = madori
        return self

    def get_madori(self):
        return self.condition.get('madori')

    def set_page(self, page):
        self.condition['page'] = page
        return self

    def get_page(self):
        return self.condition.get('page')

    def save(self):
        with open("save.data", "w") as f:
            json.dump(self.condition, f)

    def load(self):
        with open("save.data", "r") as f:
            self.condition = json.load(f)

    def clear_condition(self):
        self.condition = Context.get_initial_condition()
        return self

    @classmethod
    def get_initial_condition(cls):
        json_string = '''
        {
        "prefecture":null,
        "madori":null,
        "page":null
        }
        '''
        return json.loads(json_string)
