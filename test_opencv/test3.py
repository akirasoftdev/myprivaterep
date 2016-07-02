from test_opencv.map_analyzer import MapAnalyzer


def main():
    analyzer = MapAnalyzer()
    data_list = analyzer.analyze('work/50055.png')
    for data in data_list:
        print('%d - %d - %s' % (data['x'], data['y'], str(data['pattern'])))

    for i in range(len(data_list)):
        for j in range(i + 1, len(data_list)):
            i_char = data_list[i]
            j_char = data_list[j]
            if abs(i_char['y'] - j_char['y']) < 5 and abs(i_char['x'] - j_char['x']) < 35:
                if i_char['x'] < j_char['x']:
                    i_char['next'] = j_char
                    j_char['prev'] = i_char
                if i_char['x'] > j_char['x']:
                    j_char['next'] = i_char
                    i_char['prev'] = j_char

    for data in data_list:
        if data.get('prev') is not None:
            continue
        if data.get('next') is not None:
            text = data['pattern'].char
            while data.get('next') is not None:
                data = data['next']
                text += data['pattern'].char
            print(text)


if __name__ == '__main__':
    main()