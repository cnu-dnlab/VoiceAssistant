import os
import sys
import csv
from operator import itemgetter

from src.file_util import get_files

ARGS = None


def sync_a_b(a, b):
    am = os.path.getmtime(a)
    bm = os.path.getmtime(b)
    return bm - am


def main():
    for path in get_files(ARGS.input, ext='.mp4'):
        mp4_path = path
        pcap_path = path[:-3] + 'pcap'
        print(mp4_path, pcap_path, sync_a_b(mp4_path, pcap_path), sep=',')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input data directory')
    
    ARGS = parser.parse_args()
    main()

