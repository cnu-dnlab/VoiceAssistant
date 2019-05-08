import os
import sys
import csv
from operator import itemgetter

from src.file_util import get_files

ARGS = None


def get_stoppage(path, sts=0, ets=float('inf')):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        t1 = None
        t2 = None
        stoppage = -1
        for row in reader:
            flag = row['flag']
            ts = float(row['time'])
            if flag == 'wav': # passing wav flag
                continue
            if ts < sts:: # passing ts
                continue
            elif ets < ts:
                break
            t1 = t2
            t2 = ts
            if t1 is None or t2 is None: # passing default value
                continue
            tt_diff = t2-t1
            if stoppage < tt_diff:
                stoppage = tt_diff
    return stoppage


def get_wav_timing(path):
    wav_timing = dict()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            device_command = '-'.join((row['device'], row['command']))
            wav_timing[device_command] = \
                    {'commandStart': float(row['commandStart']),
                     'commandEnd': float(row['commandEnd']),
                     'serviceStart': float(row['serviceStart'])}
    return wav_timing


def main():
    wav_timing = dict()
    for path in get_files(ARGS.timing, ext='_wav.csv'):
        wav_timing.update(get_wav_timing(path))

    of = open(ARGS.output, 'w')
    writer = csv.writer(of)
    writer.writerow(['device', 'command', 'stoppage'])
    for path in get_files(ARGS.input, ext='.csv'):
        device_command = '.'.join((path.split('/')[-1]).split('.')[:-1])
        device, command = device_command.split('-')
        commandEnd = wav_timing[device_command]['commandEnd']
        serviceStart = wav_timing[device_command]['serviceStart']
#        try:
        stoppage = get_stoppage(path, 
            float(commandEnd), float(serviceStart))
#        except:
#            print('Error', path)

        writer.writerow([device, command, stoppage])
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

