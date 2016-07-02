# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import consts
from common.db.bukken_normalization_table import BukkenNormalizationTable
from common.db.bukken_table import BukkenTable
from common.db.station_table import StationTable
from common.db_connection_builder import DbConnectionBuilder
from common.parser import Parser
from error_rate import ErrorRate
from nn_mansion import NnMansion
from rosenka import Rosenka
import utils

LOG = logging.getLogger(__file__)
LOG.info('START')

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

rosenka = Rosenka()


@application.route('/hello', methods=['GET', 'POST'])
def hello_world():
    LOG.info('hello')
    return 'hello3'


@application.route('/address', methods=['GET'])
def get_address():
    address = request.args.get('address')
    town_id = _get_town_id(address)
    return str(town_id)


def _get_town_id(conn, address):
    return Parser.read_town_id(conn, address)


@application.route('/howmuch', methods=['GET'])
def howmuch():
    conn = DbConnectionBuilder.build(consts.HOST_NAME, consts.PORT_NO)
    try:
        address = request.args.get('address')
        occupied = request.args.get('occupied')
        walk = request.args.get('walk')
        year = request.args.get('year')
        LOG.info('address = %(address)s, occupied=%(occupied)s, walk=%(walk)s, year=%(year)s' % request.args)
        town_id = _get_town_id(conn, address)
        rosenka_price = rosenka.get(town_id)
        LOG.info('town_id = %s, rosenka_price = %s' % (town_id, rosenka_price))
        mansion_price = NnMansion.predict(year, occupied, walk, rosenka_price)
        LOG.info('mansion_price = %s' % mansion_price)
        db_year = utils.to_db_year(datetime.now().year) - int(year)
        db_occupied = int(occupied) * 100
        LOG.info('db_year = %s, db_occupied = %s' % (db_year, db_occupied))
        """
       closed_bukkens = [{
           'bukkenId': xxx,
           'townId': xxx,
           'year': xxx,
           'occupiedArea': xxx,
           'walkTime': xxx,
           'price': xxx,
           'DIFF': xxx
       }]
       """
        closed_bukkens = _find_bukkens_in_close_condition(
            conn, db_year, db_occupied, walk, town_id, rosenka_price)
        LOG.info('find bukkens in close condition')

        # error_rate
        _, stdev_error_rate, _ = ErrorRate.calculate(closed_bukkens)
        error_rate = min(stdev_error_rate, 0.5)
        LOG.info('calculate error rate')

        # [{}]
        bukken_infos = _read_bukkens(
            map(lambda x: x['bukkenId'], closed_bukkens[:5]))
        LOG.info('read bukken in close condtion')

        price_1 = mansion_price - (error_rate * mansion_price)
        price_2 = mansion_price + (error_rate * mansion_price)
        LOG.info('price_1 = ' + str(price_1))
        LOG.info('price_2 = ' + str(price_2))
        resbody = {
            'price': int(mansion_price),
            'low': int(min(price_1, price_2)),
            'high': int(max(price_1, price_2)),
            'ref': _convert_to_bukken_infos(bukken_infos)
        }
        return json.dumps(resbody, ensure_ascii=False)
    finally:
        conn.close()


def _get_mansion_price(year, occupied, walk, rosen_price):
    return NnMansion.predict(year, occupied, walk, rosen_price)


def _find_bukkens_in_close_condition(conn, year, occupied, walk, town_id, rosenka_price):
    n_year = utils.to_normalized_year(year)
    n_occupied = utils.to_normalized_occupied(occupied)
    n_walk = utils.to_normalized_walk(walk)
    n_rosenka_price = utils.to_rosenka_price(rosenka_price)
    return BukkenNormalizationTable.find(
        conn.cursor(), n_year, n_occupied, n_walk, n_rosenka_price)


def _read_bukkens(bukken_id_list):
    conn = DbConnectionBuilder.build(consts.HOST_NAME, consts.PORT_NO)
    try:
        bukken_list = []
        for bukken_id in bukken_id_list:
            bukken = BukkenTable.get(conn.cursor(), bukken_id)
            bukken_list.append(bukken)
        return bukken_list
    finally:
        conn.close()


def _read_station(conn, station_id):
    row = StationTable.get(conn.cursor(), station_id)
    return row['name']


def _convert_to_bukken_infos(rows):
    conn = DbConnectionBuilder.build(consts.HOST_NAME, consts.PORT_NO)
    try:
        bukken_infos = []
        for row in rows:
            LOG.info("stationId : " + str(row['stationId']))
            bukken_infos.append({
                'address': row['address'],
                'year': str(row['year'].year),
                'occupiedArea': (row['occupiedArea'] / 100),
                'station': _read_station(conn, row['stationId']),
                'walkTime': row['walkTime'],
                'price': row['price']
            })
        return bukken_infos
    finally:
        conn.close()


if __name__ == '__main__':
    application.run(host=consts.ALLOW_HOST)
