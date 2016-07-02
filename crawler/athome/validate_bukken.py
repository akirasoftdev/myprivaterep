# -*- coding: utf-8 -*-
import re


class ValidateBukken(object):

    @classmethod
    def validate(cls, cursor, url, title, prefecture_id, city_id, town_id, address, layout, year,
                 occupied_area, building_floors, under_ground, room_floor, structure,
                 station_id, walk_time, price, last_modified):
        if not station_id or not walk_time or not town_id or not year or not occupied_area or not price:
            raise
        if structure.find('木造') >= 0:
            return False
        return ValidateBukken.check_occupied(layout, occupied_area)

    @classmethod
    def check_occupied(cls, layout, occupied):
        r = re.compile("(\d)(.*)$")
        m = r.search(layout)
        if m is None:
            raise
        num_of_room = int(m.group(1)) + len(m.group(2))
        return (float(occupied) > num_of_room * 500) and (float(occupied) < num_of_room * 10000)

