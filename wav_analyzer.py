import os
import csv
import soundfile as sf
import numpy as np

from src.wav_util import wav_normalize, wav_mono
from src.file_util import get_files

ARGS = None
FIELDNAMES = ['device', 'command', 'callStart', 'callEnd', 
              'commandStart', 'commandEnd', 'actionStart' ,'actionEnd']


def is_talk(data, avg, std):
    """
    2-channel data
    """
    if abs(data[0] - avg)/std >= ARGS.zscore:
        return True
    else:
        return False

def binarization(data, fs):
    values = list()
    avg = np.mean(data[0:int(ARGS.buffer*fs)])
    std = np.std(data[0:int(ARGS.buffer*fs)])
    for i in range(0, len(data)):
        values.append(is_talk(data[i], avg, std))

    return values


def get_timing(input_path):
    # prepare data: preprocessing
    data, fs = sf.read(input_path, dtype='float32')
    nom_data = wav_normalize(data)
    bin_data = binarization(nom_data, fs)
    arg_data = np.argwhere(bin_data)/fs

    # calculate timing
    timing = [[arg_data[0, 0], arg_data[0, 0]]]
    for value in arg_data[:, 0]:
        if abs(timing[-1][1]-value) <= ARGS.space:
            timing[-1][1] = value
        else:
            timing.append([value, value])

    result = parse_timing(input_path, timing)

    return result

def parse_timing(filename, timing):
    result = dict()
    filename = filename.split('/')[-1]
    result = {'callStart': timing[0][0],
              'callEnd': timing[0][1],
              'commandStart': timing[1][0],
              'commandEnd': timing[1][1],
              'actionStart': timing[2][0],
              'actionEnd': timing[2][1]}
#    if (filename.startswith('googlehome') or 
#        filename.startswith('alexa')):
#        result = {'callStart': timing[0][0],
#                  'callEnd': timing[0][1],
#                  'commandStart': timing[1][0],
#                  'commandEnd': timing[1][1],
#                  'actionStart': timing[2][0],
#                  'actionEnd': timing[2][1]}
#    else:
#        result = {'callStart': timing[0][0],
#                  'callEnd': timing[0][1],
#                  'commandStart': timing[2][0],
#                  'commandEnd': timing[2][1],
#                  'actionStart': timing[3][0],
#                  'actionEnd': timing[3][1]}

    return result

def get_histogram(filename, cut_point, pad=1):
    data, fs = sf.read(filename, dtype='float32')
    nom_data = wav_normalize(data)
    mono_data = wav_mono(nom_data)
    return mono_data[:int((cut_point+pad)*fs):int(0.001*fs)]

def main():
    mode = 'w'
    if os.path.exists(ARGS.output):
        mode = 'a'
    os.makedirs(ARGS.wav_output, exist_ok=True)
    with open(ARGS.output, mode) as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if f.mode == 'w':
            writer.writeheader()
        for path in get_files(ARGS.input, ext='.wav'):
            print('Start: {0}'.format(path))
            try:
                timing = get_timing(path)
            except IndexError:
                print('Too quite: {0}'.format(path))
                continue
            filename = path.split('/')[-1]
            timing['device'] = filename.split('-')[0]
            timing['command'] = (filename.split('-')[1]).split('.')[0]
            writer.writerow(timing)
            histogram = get_histogram(path, float(timing['actionEnd']))
            filename = path.split('/')[-1]
            histname = '{0}.csv'.format('.'.join(filename.split('.')[:-1]))
            hist_path = os.path.join(ARGS.wav_output, histname)
            np.savetxt(hist_path, histogram, delimiter=',')
            print('End: {0}'.format(path))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output file')
    parser.add_argument('-w', '--wav-output',
                        type=str,
                        required=True,
                        help='Output wav histogram directory')
    parser.add_argument('-b', '--buffer',
                        type=float,
                        default=1.0,
                        help='Buffer second for calculate z-score')
    parser.add_argument('-z', '--zscore',
                        type=float,
                        default=4.0*2,
                        help='Z-Score threshold')
    parser.add_argument('-s', '--space',
                        type=float,
                        default=1.0,
                        help='Time between commands')
    ARGS = parser.parse_args()
    main()

