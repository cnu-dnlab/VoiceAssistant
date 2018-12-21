import sys

ARGS = dict()

def main():
    print(ARGS)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True,
                        help='input dir path')
    parser.add_argument('--output', type=str, required=True,
                        help='output dir path')
    ARGS = parser.parse_args()
    main()

