import os
import sys
import csv
from operator import itemgetter

from src.file_util import get_files

ARGS = None


def get_conns(path, sts=0, ets=float('inf')):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        conns = set()
        for row in reader:
            flag = row['flag']
            ts = float(row['time'])
            if flag == 'wav': # passing wav flag
                continue
            if ts < sts: # passing ts
                continue
            elif ets < ts:
                break
            p = round(float(row['point']))
            conns.add(p)
    return len(conns)


def get_wav_timing(path):
    wav_timing = dict()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            device_command = '-'.join((row['device'], row['command']))
            wav_timing[device_command] = \
                    {'callStart': float(row['callStart']),
                     'serviceEnd': float(row['serviceEnd'])}
    return wav_timing


def main():
    wav_timing = dict()
    for path in get_files(ARGS.timing, ext='_wav.csv'):
        wav_timing.update(get_wav_timing(path))

    of = open(ARGS.output, 'w')
    writer = csv.writer(of)
    writer.writerow(['device', 'command', 'conns'])
    for path in get_files(ARGS.input, ext='.csv'):
        device_command = '.'.join((path.split('/')[-1]).split('.')[:-1])
        device, command = device_command.split('-')
        callStart = wav_timing[device_command]['callStart']
        serviceEnd = wav_timing[device_command]['serviceEnd']
        conns = get_conns(path, 
            float(callStart), float(serviceEnd))

        writer.writerow([device, command, conns])
    of.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input waterfall data directory')
    parser.add_argument('-t', '--timing',
                        type=str,
                        required=True,
                        help='Input wav timing data directory')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output file')
    
    ARGS = parser.parse_args()
    main()

