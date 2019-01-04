import os
import sys
# TODO(LuHa): import multiprocessing or from multiprocessing import Pool

ARGS = None


def main():
    pass    


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tmp-dir',
                        help='tmp file directory',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output',
                        help='output file directory',
                        type=str,
                        required=True)
    ARGS = parser.parse_args()
    main()

