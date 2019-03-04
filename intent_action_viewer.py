import os
import sys
import csv
from operator import itemgetter

from src.file_util import get_files

ARGS = None


def get_voice_intent(path, thres=float('inf')):
    servers = dict()
    values = dict()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['flag'] != 'up':
                continue
            if float(row['time']) > thres:
                break
            server = round(float(row['point']))
            size = float(row['point'])-server
            servers[server] = servers.get(server, 0) + size
            if values.get(server, (0, 0))[1] < size:
                values[server] = (float(row['time']), size)

    voice_server = max(servers.items(), key=itemgetter(1))[0]
    
    intent = (0, 0)
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['flag'] != 'down':
                continue
            if round(float(row['point'])) != voice_server:
                continue
            if float(row['time']) > thres:
                break
            size = abs(float(row['point'])-voice_server)
            if intent[1] < size:
                intent = (float(row['time']), size)
    intent_timing = intent[0]

    return voice_server, intent_timing

def get_wav_timing(path):
    wav_timing = dict()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            device_command = '-'.join((row['device'], row['command']))
            wav_timing[device_command] = \
                    {'commandEnd': float(row['commandEnd']),
                     'actionStart': float(row['actionStart'])}
    return wav_timing

def main():
    wav_timing = dict()
    for path in get_files(ARGS.timing, ext='.csv'):
        wav_timing.update(get_wav_timing(path))

    print('device', 'command', 'intent', sep=',')
    for path in get_files(ARGS.input, ext='.csv'):
        device_command = '.'.join((path.split('/')[-1]).split('.')[:-1])
        device, command = device_command.split('-')
        commandEnd = wav_timing[device_command]['commandEnd']
        actionStart = wav_timing[device_command]['actionStart']
        voice_server, intent = get_voice_intent(path, 
                float(wav_timing[device_command]['actionStart']))

        print(device, command, intent, sep=',')


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
    
    ARGS = parser.parse_args()
    main()

