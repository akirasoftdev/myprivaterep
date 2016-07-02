# coding: utf-8

import os
import re

files_map = {}
files_map['0'] = os.listdir('./work/0')
files_map['1'] = os.listdir('./work/1')
files_map['2'] = os.listdir('./work/2')
files_map['3'] = os.listdir('./work/3')
files_map['4'] = os.listdir('./work/4')
files_map['5'] = os.listdir('./work/5')
files_map['6'] = os.listdir('./work/6')
files_map['7'] = os.listdir('./work/7')
files_map['8'] = os.listdir('./work/8')
files_map['9'] = os.listdir('./work/9')
files_map['a'] = os.listdir('./work/A')
files_map['b'] = os.listdir('./work/B')
files_map['c'] = os.listdir('./work/C')
files_map['d'] = os.listdir('./work/D')
files_map['e'] = os.listdir('./work/E')
files_map['f'] = os.listdir('./work/F')
files_map['g'] = os.listdir('./work/G')
files_map['z'] = os.listdir('./work/Z')

for key, files in files_map.items():
    for file in files:
        r = re.compile('^\([^)]+\)-\((\d+)\-(\d+)\)\((\d+\.\d)\-(\d+\.\d+)\-(\d+.\d+).*$')
        m = r.search(file)
        if m is None:
            continue
        h, w, area, cx, cy = m.groups()
        new_name = '%s-%s_%s_%s-%s.png' % (w,h,area,cx,cy)
        dir_name = './work/' + key + '/'
        if not os.path.exists(dir_name + new_name):
            os.rename(dir_name + file, dir_name + new_name)
        else:
            os.remove(dir_name + file)

def main():
    print()

if __name__ == '__main__':
    main()