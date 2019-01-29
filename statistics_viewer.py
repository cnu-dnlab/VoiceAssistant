import csv

from src.file_util import get_files

ARGS = None


def main():
    print('device,command,servers,ss,se')
    for path in get_files(ARGS.input, ext='.csv'):
        device = (path.split('/')[-1]).split('-')[0]
        command = ((path.split('/')[-1]).split('-')[1]).split('.')[0]
        servers = set()
        ss = 0.0
        se = 0.0
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    server = row['key'].split(':')[0]
                    servers.add(server)
                    ss_temp = (float(row['actionStart']) - 
                               float(row['commandStart']))
                    if ss_temp != 0.0:
                        ss = ss_temp
                    se_temp = (float(row['actionStart']) - 
                               float(row['commandEnd']))
                    if se_temp != 0.0:
                        se = se_temp
                except:
                    continue
        print('{0},{1},{2},{3},{4}'.format(device, command, 
                                           len(servers)-1, ss, se))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory')
    ARGS = parser.parse_args()
    main()

