# -*- coding: utf-8 -*-
import csv
import os
import re
import urllib

import shutil
import docker
import machine
import time

import numpy

from rosenka.reader import Reader


def convert_pdf_to_png(pdf, file):
    m = machine.Machine("C:\\Program Files\\Docker Toolbox\\docker-machine.exe")
    client = docker.Client(**m.config(machine='default'))
    cmd = 'convert -density 384 -quality 100 -monochrome /share/%s /share/%s' % (pdf, file)
    exec_c=client.exec_create('ubuntu', cmd)
    output=client.exec_start(exec_c)
    print(output)


def exclude_file_name(file_path):
    return file_path.rsplit('\\', 1)[1]


def move_file_to(file, to_dir):
    if not os.path.exists('%s\\%s' % (to_dir, exclude_file_name(file))):
        shutil.move(file, to_dir + '\\' + exclude_file_name(file))
        return True
    return False


def move_file(file, from_dir, to_dir):
    if not os.path.exists('%s\\%s' % (to_dir, file)):
        shutil.move('%s\\%s' % (from_dir, file), to_dir)
        return True
    return False


def result_to_file(result, file):
    with open(file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(result)


def move_files(src, dst):
    files = os.listdir(src)
    for file in files:
        try:
            if os.path.isdir(src + '\\' + file):
                continue
            if file.rsplit('.', 1)[1] == 'png':
                shutil.move(src + '\\' + file, dst)
        except:
            raise


def has_unknown_images(src):
    count = 0
    files = os.listdir(src)
    for file in files:
        if os.path.isdir(src + '\\' + file):
            continue
        if file.rsplit('.', 1)[1] == 'png':
            count += 1
    return count > 1


def remove_file(path):
    while os.path.exists(path):
        try:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
        except WindowsError:
            print("failed to remove file " + path)
            time.sleep(1)


def verify_price(price):
    r = re.compile("^\d{2,4}[a-gA-G]$")
    return r.match(price) != None


def to_int(price):
    return int(price[0:-1])


def exclude_error(prices):
    std = numpy.mean(numpy.array(prices)[:,0])
    prices = filter((lambda price: price[0] > std * 0.3 and price[0] < std * 3), prices)
    return prices

WORK_DIR='work'
SHARE_DIR='C:\\Users\\iizuka\\share_imagemagick'


def main():
    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)
    with open('pdf_list.csv', 'rb') as f:
        csv_reader = csv.reader(f)
        csv_reader.next()

        i = 0
        for row in csv_reader:
            prefecture = row[0]
            city = row[1]
            town = row[2]
            url = row[3]
            filename = url.rsplit('/', 1)[1]
            png_file_name = filename.replace('.pdf', '.png')
            csv_file_name = filename.replace('.pdf', '.csv')
            print('### ' + filename)
            if os.path.exists(WORK_DIR + '\\' + csv_file_name):
                continue

            if not os.path.exists(SHARE_DIR + '\\' + filename):
                urllib.urlretrieve(url, SHARE_DIR + '\\' + filename)
            if not os.path.exists(SHARE_DIR + '\\' + png_file_name):
                convert_pdf_to_png(filename, png_file_name)

            reader = Reader(SHARE_DIR + '\\' + png_file_name)

            pre_price_list = reader.get()
            price_list = []
            for price, x, y, w, h in pre_price_list:
                print(price)
                if verify_price(price):
                    price_list.append((to_int(price), x, y, w, h))
                else:
                    print('invalid format %s' % (price))
            if len(price_list) > 0:
                price_list = exclude_error(price_list)
            print(price_list)

            with open(WORK_DIR + '\\' + csv_file_name, 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(['price', 'x', 'y', 'width', 'height'])
                writer.writerows(price_list)

if __name__ == '__main__':
    main()