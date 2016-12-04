# -*- coding: utf-8 -*-
import numpy
import sys
import utils
import logging
from common.db_connection_builder import DbConnectionBuilder
from nn_mansion import NnMansion
from rosenka import Rosenka
logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.info('START')

class ErrorRate:

    @staticmethod
    def calculate(bukkens):
        """
        :param bukkens: [{'townId':xxx, 'year':xxx, 'occupiedArea': xxx, 'walkTime': xxx, 'price': xxx}]
        :return: error_rate
        """
        cls = ErrorRate
        # nn_params = [[year, occupiedArea, walkTime, rosenka], ...]
        nn_params = cls._convert_to_nn_params(bukkens)
        # predict_array = [prediction price, ...]
        predict_prices = NnMansion.predict_by_array(nn_params)
        # actual_array = [actual price, ...]
        actual_prices = numpy.float32(map(lambda x: x['price'], bukkens))
        # error_rate_array = [error rate, ...]
        error_rates = abs(actual_prices - predict_prices) / actual_prices
        stdev_error_rate = numpy.std(error_rates)
        mean_error_rate = numpy.mean(error_rates)
        LOG.info('stdev_error_rates : %s' % stdev_error_rate)
        LOG.info('mean_error_rates : %s' % mean_error_rate)
        return error_rates, stdev_error_rate, mean_error_rate

    @staticmethod
    def _convert_to_nn_params(bukkens):
        rosenka = Rosenka()
        in_params = []
        for bukken in bukkens:
            town_id = bukken['townId']
            rosenka_price = rosenka.get(town_id)
            in_params.append([
                utils.to_nn_year_from_db(bukken['year'].year),
                utils.to_nn_occupied_from_db(bukken['occupiedArea']),
                utils.to_nn_walk_time_from_db(bukken['walkTime']),
                utils.to_nn_rosenka_price_from_db(rosenka_price)
            ])
        return in_params


def query_bukken(conn, last_modified):
    """
    :return:
    """

    sql = '''
    select
        townId, year, occupiedArea, walkTime, price
    from
        bukken
    where
        lastModified = %(last_modified)s
    '''
    params = {
        'last_modified': last_modified
    }
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()


def count_of_error_rate(error_rate_list, low, high):
    f_list = filter(lambda x: low <= x < high, error_rate_list)
    return len(f_list)


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    last_modified = sys.argv[3]
    LOG.info('host_name = ' + host_name)
    LOG.info('port_no = ' + port_no)
    LOG.info('last_modified = ' + last_modified)

    conn = DbConnectionBuilder.build(host_name, port_no)
    bukkens = query_bukken(conn, last_modified)
    error_rates, stdev_error_rate, mean_error_rate = ErrorRate.calculate(bukkens)

    for low in range(0, 10, 1):
        count = count_of_error_rate(error_rates, 0, float(low+1) / 10)
        if count > 0:
            LOG.info('%s: %s (%s)' % (low, count, (float(count * 100) / len(error_rates))))
    LOG.info('total = %s' % (len(error_rates)))

    conn.close()

if __name__ == '__main__':
    main()