import csv

from src.file_util import get_files

ARGS = None


def main():
    for path in get_files(ARGS.input, ext='.csv'):
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print('{0},{1},{2},{3}'.format(row['device'],
                                               row['command'],
                                               float(row['actionStart'])-
                                               float(row['commandStart']),
                                               float(row['actionStart'])-
                                               float(row['commandEnd'])))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory')
    ARGS = parser.parse_args()
    main()

