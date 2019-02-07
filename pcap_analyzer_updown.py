import os
import csv
import copy
import subprocess

from src.file_util import get_files, make_dirs
from src.pcap_util import export_pcap_updown


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

def get_output_path(path):
    filepath = path.split('/')[-1]
    filepath = filepath.split('.')[0] + '.csv'
    return os.path.join(ARGS.output, filepath)

def main():
    # make output dir
    make_dirs(ARGS.output)

    wav_data = get_wav_data(ARGS.timing) 
    # analyze file by file
    for path in get_files(ARGS.input, ext='.pcap'):
        print('Start: {0}'.format(path))
        device_command = (path.split('/')[-1]).split('.')[0]
        output_path = get_output_path(path)
        try:
            export_pcap_updown(path, output_path, 
                               float(wav_data[device_command]['actionEnd']))
        except KeyError:
            print('Invalid wav csv: {0}'.format(path))
            continue
        print('Done: {0}'.format(output_path))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory')
    parser.add_argument('-t', '--timing',
                        type=str,
                        required=True,
                        help='Input file wav timing')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output directory')
    ARGS = parser.parse_args()

    main()

