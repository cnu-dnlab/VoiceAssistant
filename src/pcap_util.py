import csv

from operator import itemgetter

from pcap_to_csv import PcapToCSV
from flow_timing import FlowTiming
from updown_timing import UpDownTiming
from sync_util import sync_a_b

TIMING_ORDER = ['domainLookupStart', 'domainLookupEnd',
                'connectStart', 'connectEnd',
                'secureConnectionStart', 'requestStart',
                'responseStart', 'responseEnd']


def export_pcap_timing(pcap_path, csv_path):
    pcap_reader = PcapToCSV(pcap_path, remove=True)
    flow_timer = FlowTiming(pcap_reader.get_csv_path())
    flow = flow_timer.get_flow_timing()
    result = list()

    for key in flow.keys():
        item = flow[key]
        draw = dict()
        draw['key'] = key
        is_write = False
        for timing in TIMING_ORDER:
            data = item.get(timing, str(0.0))
            draw[timing] = data
            # if data != '0.0':
                # is_write = True
        # if is_write:
        result.append(draw)

    result.sort(key=itemgetter('domainLookupStart', 'key'), reverse=True)

    with open(csv_path, 'w') as f:
        fieldnames = ['key'] + TIMING_ORDER
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(result)

def export_pcap_updown(pcap_path, csv_path):
    wav_path = '{0}.wav'.format('.'.join(pcap_path.split('.')[:-1]))
    sync_time = sync_a_b(pcap_path, wav_path)
    pcap_reader = PcapToCSV(pcap_path, remove=True)
    updown_timer = UpDownTiming(pcap_reader.get_csv_path())
    flow = updown_timer.get_updown_timing()
    result = dict()

    updown_keys = list(flow.keys())
    updown_keys.sort()
    for key in flow.keys():
        for time_rel, data in flow[key]:
            time_rel = float(time_rel) + sync_time
            item = result.get(time_rel, [-1, -1, -1, -1])
            pos = updown_keys.index(key)+1
            if int(data) > 0:
                item[0] = pos
                item[1] = int(data)
            else:
                item[2] = pos
                item[3] = int(data)
            result[time_rel] = item

    items = list(result.items())
    items.sort()

    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'up', 'updata', 'down', 'downdata'])
        for item in items:
            row = [item[0]] + item[1]
            if row[3] != -1:
                row[4] = -row[4]
            writer.writerow(row)

    with open(csv_path+'.head', 'w') as f:
        writer = csv.writer(f)
        for key in updown_keys:
            writer.writerow([key])

