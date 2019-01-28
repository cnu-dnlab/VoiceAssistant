import csv

from operator import itemgetter

from pcap_to_csv import PcapToCSV
from flow_timing import FlowTiming

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
