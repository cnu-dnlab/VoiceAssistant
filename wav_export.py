import os
import soundfile as sf
import numpy as np

from src.wav_util import wav_normalize, wav_mono

ARGS = None


def get_histogram(filename, cut_point, pad=1):
    data, fs = sf.read(filename, dtype='float32')
    nom_data = wav_normalize(data)
    mono_data = wav_mono(nom_data)
    return mono_data[:int((cut_point+pad)*fs):int(0.001*fs)]


def main():
    path = os.path.abspath(os.path.expanduser(ARGS.input))
    histogram = get_histogram(path, ARGS.end)
    filename = path.split('/')[-1]
    histname = '{0}.csv'.format('.'.join(filename.split('.')[:-1]))
    hist_path = os.path.join(ARGS.output, histname)
    np.savetxt(hist_path, histogram, delimiter=',')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input file')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output directory')
    parser.add_argument('-e', '--end',
                        type=float,
                        required=True,
                        help='end point')
    ARGS = parser.parse_args()
    main()

