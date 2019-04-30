import subprocess
import shlex
import re
import csv
import os

from src.file_util import get_files, std_path
from src.print_util import pprint

FLAGS = None


def get_tcptrace(path):
    command_line = 'tcptrace -nul \'{0}\''.format(path)
    command = shlex.split(command_line)
    cp = subprocess.run(command, stdout=subprocess.PIPE, 
                                 stderr=subprocess.DEVNULL,
                                 universal_newlines=True)
    return cp.stdout


def get_hosts(conn):
    hosts = re.findall('(?:host \w+:\s+)([\d|.|:]+)', conn)
    if len(hosts) == 2:
        return hosts
    else:
        return None, None


def get_complete_conn(conn):
    complete_conn = re.findall('(?:complete conn:\s+)(\w+)', conn)
    if len(complete_conn) > 0:
        return complete_conn[0]
    else:
        return None


def get_attributes(conn, attr):
    regex = '(?:{0}:\s+)(\d+)'.format(attr)
    attrs = re.findall(regex, conn)
    return attrs


def main(_):
    pprint('Start tcptrace viewer')

    # prepare output file
    if os.path.exists(FLAGS.output):
        of = open(FLAGS.output, 'a')
    else:
        of = open(FLAGS.output, 'w')
    writer = csv.writer(of)
    if of.mode == 'w':
        writer.writerow(['device', 'command', 'host1', 'host2', 'comp_conn', 
                         'total_packets', 'bytes_sent', 'avg_win_adv'])

    # Loop pcap files
    for path in get_files(FLAGS.input, ext='.pcap'):
        pprint('Processing pcap file: {0}'.format(path))
        # get device and command
        device_command = path.split('/')[-1]
        device_command = device_command.split('.')[0]
        device, command = device_command.split('-')
        # get tcptrace result using subprocess
        result_line = get_tcptrace(path)
        # remove the header, first five lines
        result_line = '\n'.join(result_line.split('\n')[8:])
        # get connections
        conns = result_line.split('================================')
        # print information: export csv
        for conn in conns:
            host1, host2 = get_hosts(conn)
            if host1 is None:
                continue
            comp_conn = get_complete_conn(conn)
            total_packets = get_attributes(conn, 'total packets')
            bytes_sent = get_attributes(conn, 'unique bytes sent')
            avg_win_adv = get_attributes(conn, 'avg win adv')
            writer.writerow([device, command, host1, host2, comp_conn, 
                             total_packets, bytes_sent, avg_win_adv])

    pprint('End tcptrace viewer')
    of.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='Pcap directory')
    parser.add_argument('-o', '--output', type=str,
                        help='tcptrace analysis output file path')
    FLAGS, _ = parser.parse_known_args()

    FLAGS.output = std_path(FLAGS.output)

    main(_)

