import codecs
import csv


class ReadRosenka(object):
    @classmethod
    def read(cls, file_name):
        sum = 0
        count = 0
        with codecs.open(file_name, 'r', 'utf8', 'ignore') as f:
            for price, _, _, _, _ in csv.reader(f):
                if price == 'price':
                    continue
                sum += int(price)
                count += 1
        if sum == 0:
            return 0
        return int(sum / count)