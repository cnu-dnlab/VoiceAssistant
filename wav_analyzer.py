import soundfile as sf
import numpy as np

ARGS = None


def main():
    data, fs = sf.read(ARGS.input, dtype='float32')
    arg_list = list(np.argwhere(data>data.max()*0.5)[:,0]/44100)
    arg_set = set()
    for entry in arg_list:
        time_float = '{0:.3f}'.format(entry)
        arg_set.add(float(time_float))
    time_list = list(arg_set)
    time_list.sort()
    btime = -1
    time_result = list()
    for entry in time_list:
        if abs(btime - entry) < 1:
            btime = entry
            continue
        else:
            btime = entry
            time_result.append(entry)
    print(time_result)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input file')
    ARGS = parser.parse_args()
    main()

