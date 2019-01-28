import os
import csv

from src.file_util import get_files

ARGS = None
FIELDNAMES = ['key', 'callStart', 'callEnd', 'commandStart', 'commandEnd',
              'actionStart', 'actionEnd', 'domainLookupStart',
              'domainLookupEnd', 'connectStart', 'connectEnd',
              'secureConnectionStart', 'requestStart', 'responseStart',
              'responseEnd', 'white']


def get_wav_data(path):
    data = dict()

    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = '-'.join((row['device'], row['command']))
            value = {'callStart': row['callStart'],
                     'callEnd': row['callEnd'],
                     'commandStart': row['commandStart'],
                     'commandEnd': row['commandEnd'],
                     'actionStart': row['actionStart'],
                     'actionEnd': row['actionEnd']}
            data[key] = value

    return data

def get_min(data):
    result = float('inf')
    for value in data.values():
        try:
            float_value = float(value)
        except ValueError:
            continue
        if float_value != 0.0 and result > float_value:
            result = float_value

    return result


def main():
    # create output directory
    os.makedirs(ARGS.output, exist_ok=True)
    
    wav_data = get_wav_data(ARGS.wav_input)
    for path in get_files(ARGS.pcap_input, ext='.csv'):
        print('Start: {0}'.format(path))
        filename = path.split('/')[-1]
        output_path = os.path.join(ARGS.output, filename)
        with open(output_path, 'w') as of:
            writer = csv.DictWriter(of, fieldnames=FIELDNAMES)
            writer.writeheader()
            key = filename.split('.')[0]
            try:
                white = get_min(wav_data[key])
                data = {'key': key, 
                        'callStart': wav_data[key]['callStart'], 
                        'callEnd': wav_data[key]['callEnd'], 
                        'commandStart': wav_data[key]['commandStart'], 
                        'commandEnd': wav_data[key]['commandEnd'],
                        'actionStart': wav_data[key]['actionStart'], 
                        'actionEnd': wav_data[key]['actionEnd'], 
                        'domainLookupStart': 0, 'domainLookupEnd': 0, 
                        'connectStart': 0, 'connectEnd': 0,
                        'secureConnectionStart': 0, 'requestStart': 0, 
                        'responseStart': 0, 'responseEnd': 0,
                        'white': white}
            except KeyError:
                print('Something not found', key)
                continue
            writer.writerow(data)
            with open(path, 'r') as rf:
                reader = csv.DictReader(rf)
                for row in reader:
                    row.update({'callStart': 0, 'callEnd': 0,
                                'commandStart': 0, 'commandEnd': 0,
                                'actionStart': 0, 'actionEnd': 0})
                    white = get_min(row)
                    row['white'] = white
                    writer.writerow(row)
        print('Done: {0}'.format(path))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wav-input',
                        type=str,
                        required=True,
                        help='Input file after wav analysis')
    parser.add_argument('-p', '--pcap-input',
                        type=str,
                        required=True,
                        help='Input directory after pcap analysis')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output directory')
    ARGS = parser.parse_args()
    main()

