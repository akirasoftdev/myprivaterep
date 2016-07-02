# -*- coding: utf-8 -*-
import numpy


def to_normalized_year(year):
    """
    平均     標準偏差
    31.1387  7.914659544237533
    """
    return (float(year) - 31.1387) / 7.914659544237533


def to_normalized_occupied(occupied):
    """
    平均         標準偏差
    6486.1952    2117.5691044636487
    """
    return (float(occupied) - 6486.1952) / 2117.5691044636487


def to_normalized_walk(walk):
    """
    平均         標準偏差
    10.0463      7.09756102948334
    """
    return (float(walk) - 10.0463) / 7.09756102948334


def to_rosenka_price(rosenka_price):
    """
    平均         標準偏差
    365.8280     399.1240927984568
    """
    return (float(rosenka_price) - 365.8280) / 399.1240927984568


def to_db_year(year):
    return int(year - 1970)


def to_db_occupied(occupied):
    return int(occupied * 100)


def to_nn_year_from_db(db_year):
    return numpy.float32(db_year - 1970)


def to_nn_occupied_from_db(db_occupied):
    return numpy.float32(db_occupied) / 100


def to_nn_walk_time_from_db(db_walk_time):
    return numpy.float32(db_walk_time)


def to_nn_rosenka_price_from_db(db_rosenka_price):
    return numpy.float32(db_rosenka_price)