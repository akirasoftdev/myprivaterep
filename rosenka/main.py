# -*- coding: utf-8 -*-
import csv
import re

import numpy

from reader import Reader


def verify_price(price):
    r = re.compile("^\d{2,4}[a-gA-G]$")
    return r.match(price) != None


def to_int(price):
    return int(price[0:-1])


def exclude_error(prices):
    std = numpy.mean(numpy.array(prices)[:,0])
    prices = filter((lambda price: price[0] > std * 0.3 and price[0] < std * 3), prices)
    return prices


def main():
    reader = Reader('../test_opencv/work/50055.png')
    pre_price_list = reader.get()
    price_list = []
    for price, x, y, w, h in pre_price_list:
        print(price)
        if verify_price(price):
            price_list.append((to_int(price), x, y, w, h))
        else:
            print('invalid format %s' % (price))
    price_list = exclude_error(price_list)
    print(price_list)

    with open('test.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['price', 'x', 'y', 'width', 'height'])
        writer.writerows(price_list)

if __name__ == "__main__":
    main()
