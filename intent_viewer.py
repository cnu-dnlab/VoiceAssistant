import os
import sys
import csv
from operator import itemgetter

from src.file_util import get_files

ARGS = None


def get_voice_intent(path, sth=0, mth=0, eth=float('inf')):
    servers = dict()
    values = dict()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['flag'] != 'up':
                continue
            if float(row['time']) > eth:
                break
            server = round(float(row['point']))
            size = float(row['point'])-server
            servers[server] = servers.get(server, 0) + size
            if values.get(server, (0, 0))[1] < size:
                values[server] = (float(row['time']), size)

    voice_server = max(servers.items(), key=itemgetter(1))[0]
    
    intent = sth
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        down_set = set()
        for row in reader:
            if row['flag'] != 'down':
                continue
            if round(float(row['point'])) != voice_server:
                continue
            if float(row['time']) < sth:
                continue
            if float(row['time']) > eth:
                break
            size = abs(float(row['point'])-voice_server)
            if float(row['time']) <= mth:
                down_set.add(size)
                continue
            if size not in down_set:
                intent = float(row['time'])
                break
    return voice_server, intent

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
    for path in get_files(ARGS.timing, ext='.csv'):
        wav_timing.update(get_wav_timing(path))

    of = open(ARGS.output, 'w')
    writer = csv.writer(of)
    writer.writerow(['device', 'command', 'intent'])
    for path in get_files(ARGS.input, ext='.csv'):
        device_command = '.'.join((path.split('/')[-1]).split('.')[:-1])
        device, command = device_command.split('-')
        commandStart = wav_timing[device_command]['commandStart']
        commandEnd = wav_timing[device_command]['commandEnd']
        serviceStart = wav_timing[device_command]['serviceStart']
        voice_server, intent = get_voice_intent(path, 
          float(commandStart), float(commandEnd), float(serviceStart))

        writer.writerow([device, command, intent])
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

