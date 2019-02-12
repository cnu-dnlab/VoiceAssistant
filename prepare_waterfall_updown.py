import os
import csv
import shutil

import numpy as np

from src.file_util import get_files

ARGS = None
FIELDNAMES = ['time', 'point']


def get_wav_data(path):
    data = dict()

    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = '-'.join((row['device'], row['command']))
            value = {'callStart': row['callStart'],
                     'callEnd': row['callEnd'],
                     'commandStart': row['commandStart'],
                     'commandEnd': row['commandEnd'],
                     'actionStart': row['actionStart'],
                     'actionEnd': row['actionEnd']}
            data[key] = value

    return data

def get_min(data):
    result = float('inf')
    for value in data.values():
        try:
            float_value = float(value)
        except ValueError:
            continue
        if float_value != 0.0 and result > float_value:
            result = float_value

    return result


def main():
    # create output directory
    os.makedirs(ARGS.output, exist_ok=True)
    
    wav_data = get_wav_data(ARGS.timing)
    for path in get_files(ARGS.pcap_input, ext='.csv'):
        # Data prepare
        pcap_path = path
        hist_path = os.path.join(ARGS.wav_input, path.split('/')[-1])
        if not os.path.exists(hist_path):
            print('Hist file not exists: {0}'.format(hist_path))
            continue
        device_command = (path.split('/')[-1]).split('.')[0]
        print('Start: {0}'.format(device_command))
        database = dict()
        with open(pcap_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ttime = float(row['time'])
                while ttime in database.keys():
                    ttime = ttime + 1e-9
                if row['up'] != '-1':
                    point = int(row['up']) + (int(row['updata'])/1460*0.45)
                    flag = 'up'
                elif row['down'] != '-1':
                    point = int(row['down']) - (int(row['downdata'])/1460*0.45)
                    flag = 'down'
                elif row['syn'] != '-1':
                    flag = 'syn'
                elif row['fin'] != '-1':
                    flag = 'fin'
                elif row['ssl'] != '-1':
                    flag = 'ssl'
                elif row['dns'] != '-1':
                    flag = 'dns'
                    
                data = {'time': ttime,
                        'point': point}
                database[ttime] = data
        with open(hist_path, 'r') as f:
            reader = csv.reader(f)
            ttime = float(0)
            for row in reader:
                while ttime in database.keys():
                    ttime = ttime + 1e-9
                point = float(row[0])*0.45
                data = {'time': ttime,
                        'point': point}
                database[ttime] = data
                ttime = ttime + 0.001
        # Data sorting
        export = list()
        keys = list(database.keys())
        keys.sort()
        for key in keys:
            export.append(database[key])
        # Data export
        filename = path.split('/')[-1]
        output_path = os.path.join(ARGS.output, filename)
        with open(output_path, 'w') as of:
            writer = csv.DictWriter(of, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(export)

        # Head file
        head_src = '.'.join(path.split('.')[:-1])+'.head'
        head_dst = os.path.join(ARGS.output, head_src.split('/')[-1])
        shutil.copy2(head_src, head_dst)

        # line file
        filename = '.'.join((path.split('/')[-1]).split('.')[:-1])+'.line'
        line_path = os.path.join(ARGS.output, filename)
        with open(line_path, 'w') as lf:
            writer = csv.writer(lf)
            for timing in ['callStart', 'callEnd',
                           'commandStart', 'commandEnd',
                           'actionStart', 'actionEnd']:
                writer.writerow([wav_data[device_command][timing]])
        print('Done: {0}'.format(path))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timing',
                        type=str,
                        required=True,
                        help='Input file wav timing analysis')
    parser.add_argument('-w', '--wav-input',
                        type=str,
                        required=True,
                        help='Input directory after wav analysis')
    parser.add_argument('-p', '--pcap-input',
                        type=str,
                        required=True,
                        help='Input directory after pcap analysis')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output directory')
    ARGS = parser.parse_args()
    main()

