import os
import csv

import numpy as np

from src.file_util import get_files

ARGS = None
FIELDNAMES = ['time', 'up', 'updata', 'down', 'downdata',
              'soundon']


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
    
    wav_data = get_wav_data(ARGS.wav_input)
    for path in get_files(ARGS.pcap_input, ext='.csv'):
        print('Start: {0}'.format(path))
        filename = path.split('/')[-1]
        output_path = os.path.join(ARGS.output, filename)
        with open(output_path, 'w') as of:
            writer = csv.DictWriter(of, fieldnames=FIELDNAMES)
            writer.writeheader()
            key = filename.split('.')[0]
            try:
                wav_item = wav_data[key]
                max_time = float(wav_item['actionEnd']) + 1
                for seq in np.arange(float(wav_item['callStart']), 
                                     float(wav_item['callEnd']), 
                                     0.001):
                    data = {'time': seq,
                            'up': -1,
                            'updata': -1,
                            'down': -1,
                            'downdata': -1,
                            'soundon': 0}
                    writer.writerow(data)
                for seq in np.arange(float(wav_item['commandStart']), 
                                     float(wav_item['commandEnd']), 
                                     0.001):
                    data = {'time': seq,
                            'up': -1,
                            'updata': -1,
                            'down': -1,
                            'downdata': -1,
                            'soundon': 0}
                    writer.writerow(data)
                for seq in np.arange(float(wav_item['actionStart']), 
                                     float(wav_item['actionEnd']), 
                                     0.001):
                    data = {'time': seq,
                            'up': -1,
                            'updata': -1,
                            'down': -1,
                            'downdata': -1,
                            'soundon': 0}
                    writer.writerow(data)
            except KeyError:
                print('Something not found', key)
                continue
            with open(path, 'r') as rf:
                reader = csv.DictReader(rf)
                for row in reader:
                    if float(row['time']) > max_time:
                        break
                    row.update({'soundon': -1})
                    writer.writerow(row)
        print('Done: {0}'.format(path))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wav-input',
                        type=str,
                        required=True,
                        help='Input file after wav analysis')
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

