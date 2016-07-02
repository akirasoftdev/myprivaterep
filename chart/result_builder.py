# -*- coding: utf-8 -*-
import sys
import os
import numpy
import matplotlib
import pandas

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from common.db_connection_builder import DbConnectionBuilder

matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from chart.result_table import ResultTable

font = ['family', 'sans-serif']

def create_price_line_chart(error_rate, prices):
    plt.hold(False)
#    plt.style.use('ggplot')
    if font is None:
        plt.rc('font', **font)
    plt.scatter(error_rate, prices)
    plt.title('price')
    plt.xlabel('relative_error')
    plt.ylabel('price')
    plt.savefig("price.png")

def create_year_line_chart(error_rate, year_values):
    plt.hold(False)
#    plt.style.use('ggplot')
    if font is None:
        plt.rc('font', **font)
    plt.scatter(error_rate, year_values)
    plt.title('building_year')
    plt.xlabel('relative_error')
    plt.ylabel('month')
#    plt.xlim([0, 2])
    plt.ylim([0, 50])
    plt.savefig("year.png")

def create_occupied_line_chart(error_rate, occupied_values):
    plt.hold(False)
#    plt.style.use('ggplot')
    if font is None:
        plt.rc('font', **font)
    plt.scatter(error_rate, occupied_values)
    plt.title('occupied')
    plt.xlabel('relative_error')
    plt.ylabel('occupied')
#    plt.xlim([0, 2])
    plt.savefig("occupied.png")


def create_walk_line_chart(error_rate, walk_values):
    plt.hold(False)
#    plt.style.use('ggplot')
    if font is None:
        plt.rc('font', **font)
    plt.scatter(error_rate, walk_values)
    plt.title('walk')
    plt.xlabel('relative_error')
    plt.ylabel('walk')
#    plt.xlim([0, 2])
    plt.savefig("walk.png")


def create_posted_line_chart(error_rate, posed_values):
    plt.hold(False)
#    plt.style.use('ggplot')
    if font is None:
        plt.rc('font', **font)
    plt.scatter(error_rate, posed_values)
    plt.title('posted')
    plt.xlabel('relative_error')
    plt.ylabel('posted')
#    plt.xlim([0, 2])
    plt.savefig("posted.png")

def create_rosenka_line_chart(error_rate, rosenka_values):
    plt.hold(False)
#    plt.style.use('ggplot')
    if font is None:
        plt.rc('font', **font)
    plt.scatter(error_rate, rosenka_values)
    plt.title('rosen')
    plt.xlabel('relative_error')
    plt.ylabel('rosen')
#    plt.xlim([0, 2])
    plt.ylim([0, 6000])
    plt.savefig("rosenka.png")


def create_pie_chart(values):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.pie(values,
           labels=['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '100%over'],
           autopct='%.1f%%', startangle=90)
    plt.savefig("piechart.png")

def calculate_rates(relative_error):
    error_rates = []
    for r in range(1, 11, 1):
        s = float(r) / 10
        print(s)
        error_rates.append(
            numpy.round(
                relative_error[relative_error[relative_error > (s - 0.1)] <= s].size * 100 / relative_error.size)
        )
    error_rates.append(numpy.round(relative_error[relative_error > 1.0].size * 100 / relative_error.size))
    return error_rates


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    csv_file = sys.argv[3]
    build_no = sys.argv[4]

    # CSV データを読み込む
    macro = pandas.read_csv(csv_file)
    relative_error = macro.values[:, 0]
    prices = macro.values[:, 2]
    year_values = macro.values[:, 3]
    occupied_values = macro.values[:, 4]
    walk_values = macro.values[:, 5]
    posted_values = macro.values[:, 6]
    rosenka_values = macro.values[:, 7]

    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()

    rates = calculate_rates(relative_error)
    average = numpy.average(relative_error.astype(float))
    ResultTable.register(cursor, build_no, average, rates)

    connection.commit()
    connection.close()
    create_pie_chart(rates)

    create_price_line_chart(relative_error, prices)
    create_year_line_chart(relative_error, year_values)
    create_occupied_line_chart(relative_error, occupied_values)
    create_walk_line_chart(relative_error, walk_values)
    create_posted_line_chart(relative_error, posted_values)
    create_rosenka_line_chart(relative_error, rosenka_values)


if __name__ == "__main__":
    main()
