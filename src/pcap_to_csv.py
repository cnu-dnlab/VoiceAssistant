import os
import csv
import subprocess


class PcapToCSV(object):
    def __init__(self, pcap_path, max_time, remove=False):
        self.pcap_path = pcap_path
        self.max_time = max_time
        self.csv_path = self._execute_tshark()
        self.remove = remove

    def __del__(self):
        if self.remove:
            if os.path.exists(self.csv_path):
                os.remove(self.csv_path)

    def _execute_tshark(self):
        pcap_path = self.pcap_path
        csv_path = '.'.join((pcap_path.split('.'))[:-1]) + '.csv'
        command = ('tshark -Y "(tcp or udp) and (frame.time_relative<={2:.9f})" '
                   '-T fields '
                   '-e frame.time_relative -e ip.proto -e ip.src '
                   '-e ip.len '
                   '-e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport '
                   '-e tcp.flags.syn -e tcp.flags.ack -e tcp.flags.fin '
                   '-e tcp.flags.push '
                   '-e tcp.len -e udp.length '
                   '-e ssl.handshake '
                   '-e dns.a -e dns.qry.name '
                   '-E header=y -E separator=, '
                   '-E quote=d '
                   '-r {0} > {1}').format(self.pcap_path, csv_path, self.max_time)
        subprocess.run(command, shell=True)
        return csv_path

    def get_csv_path(self):
        return self.csv_path
