import os
import soundfile as sf
import numpy as np

ARGS = None


def get_files(path, ext='', recursive=False):
    path_list = [path]
    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        yield entry.path
                    else:
                        if recursive:
                            path_list.append(entry.path)


def get_timing(input_path):
    data, fs = sf.read(input_path, dtype='float32')
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
        if abs(btime - entry) < 0.1:
            btime = entry
            continue
        else:
            btime = entry
            time_result.append(entry)
    return time_result


def main():
    result = list()
    for path in get_files(ARGS.input, ext='.wav'):
        timing = get_timing(path)
        result.append((path, timing))
    result.sort()
    for key, value in result:
        print('{0:>18s} {1}'.format(key[2:], value))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input file')
    ARGS = parser.parse_args()
    main()

