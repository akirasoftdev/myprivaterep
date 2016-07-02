# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from chart.result_table import ResultTable
from common.db_connection_builder import DbConnectionBuilder

host_name = sys.argv[1]
port_no = sys.argv[2]
build_no = sys.argv[3]

connection = DbConnectionBuilder.build(host_name, port_no)
cursor = connection.cursor()

result = ResultTable.read(cursor, build_no)
if result is not None:
    f = open('result_rate.csv', 'w')
    f.write('20%, 40%, 60%, 80%, 100%, over\n')
    f.write('%d, %d, %d, %d, %d, %d\n' % (
            (result['error_rate_1'] + result['error_rate_2']),
            (result['error_rate_3'] + result['error_rate_4']),
            (result['error_rate_5'] + result['error_rate_6']),
            (result['error_rate_7'] + result['error_rate_8']),
            (result['error_rate_9'] + result['error_rate_10']),
            (result['error_rate_over'])))
    f.flush()
    f.close()

    f = open('result_total.csv', 'w')
    f.write('total\n')
    f.write('%s\n' % (result['total_error_rate']))
    f.flush()
    f.close()