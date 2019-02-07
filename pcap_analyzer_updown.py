import os
import csv
import copy
import subprocess

from src.file_util import get_files, make_dirs
from src.pcap_util import export_pcap_updown


def get_output_path(path):
    filepath = path.split('/')[-1]
    filepath = filepath.split('.')[0] + '.csv'
    return os.path.join(ARGS.output, filepath)

def main():
    # make output dir
    make_dirs(ARGS.output)

    # analyze file by file
    for path in get_files(ARGS.input, ext='.pcap'):
        print('Start: {0}'.format(path))
        output_path = get_output_path(path)
        export_pcap_updown(path, output_path)
        print('Done: {0}'.format(output_path))


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
                        help='Output directory')
    ARGS = parser.parse_args()

    main()

