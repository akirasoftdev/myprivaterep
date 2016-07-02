import os
import re

import shutil

from test_opencv.load_pattern import LoadPattern
from test_opencv.pattern import Pattern

patterns = LoadPattern().load()

def main():
    DIR = 'work/u/'
    files = os.listdir(DIR)
    for file in files:
        if not os.path.isdir(DIR + file):
            continue
        file2s = os.listdir(DIR + file)
        print("%s = %d" % ((DIR + file), len(file2s)))
        for file2 in file2s:
            print("%s" % file2)
            r = re.compile('^\([^)]+\)-\((\d+)\-(\d+)\)\((\d+\.\d)\-(\d+\.\d+)\-(\d+.\d+).*$')
            try:
                h,w,area,cx,cy = r.search(file2).groups()
            except AttributeError:
                continue
            key = Pattern.to_key(w, h, area, cx, cy)
            if key in patterns:
                print(' ##### %s ' % key)
                os.remove(DIR + file + '/' + file2)

        file2s = os.listdir(DIR + file)
        if len(file2s) < 2:
            shutil.rmtree(DIR + file)

if __name__ == "__main__":
    main()