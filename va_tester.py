import csv
import os
import subprocess
import shlex
import time
import signal

from scenario_func import get_scenario, play_scenario

ARGS = None
CONFIG = None


def parse_input(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['dev'], row['cat'], row['com'], row['sce']


def main(_):
    # set collector path
    croot = os.path.abspath(os.path.expanduser(CONFIG['Collector']['Path']))
    cpcap = os.path.join(croot, 'vapm_collector_pcap.py')
    cmp4 = os.path.join(croot, 'vapm_collector_mp4.py')

    # get scenario path
    sroot = os.path.abspath(os.path.expanduser(CONFIG['Scenario']['Path']))

    # get command path
    mroot = os.path.abspath(os.path.expanduser(CONFIG['Command']['Path']))

    # setting output directory
    odir = os.path.abspath(os.path.expanduser(ARGS.output))
    os.makedirs(odir, mode=0o755, exist_ok=True)

    # loop
    ## setting input file
    icsv = os.path.abspath(os.path.expanduser(ARGS.input))
    for dev, cat, com, sce in parse_input(icsv):
        cpath = '-'.join([dev, cat, com])
        ## Start collector
        ### pcap
        foname = '{0}.pcap'.format(cpath)
        opath = os.path.join(odir, foname)
        cmd = ('python3 {0} -t /tmp/temp.pcap -r {1} -e {2} -o {3}').format(
                 cpcap, ARGS.router_ip, ARGS.exclude_ip, opath)
        proc_pcap = subprocess.Popen(shlex.split(cmd), 
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
        ### mp4
        foname = '{0}.mp4'.format(cpath)
        opath = os.path.join(odir, foname)
        cmd = ('python3 {0} -t /tmp/temp.mp4 -d {1} -i {2} -o {3}').format(
                 cmp4, ARGS.video_dev, ARGS.audio_idx, opath)
        proc_mp4 = subprocess.Popen(shlex.split(cmd), 
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)

        ### wait for 3 seconds to execute collector completly
        time.sleep(3)

        ## Play scenario
        data = {'dev': dev, 'cat': cat, 'com': com, 
                'mroot': mroot, 'cpath': cpath}
        scene = get_scenario(sroot, sce)
        play_scenario(scene, data)

        ## Stop collector and archive data
        proc_pcap.send_signal(signal.SIGINT)
        proc_mp4.send_signal(signal.SIGINT)

        print('Done: {0}'.format(cpath))
        ### wait for 2 seconds to archive data and delimit
        time.sleep(2)


if __name__ == '__main__':
    import configparser

    CONFIG = configparser.ConfigParser()
    CONFIG.read('config.ini')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='input command csv',
                        required=True)
    parser.add_argument('-o', '--output', type=str,
                        help='output file directory',
                        required=True)
    parser.add_argument('-s', '--scenario', type=str,
                        help='scenario file directory',
                        default='./scenario')
    parser.add_argument('-e', '--exclude-ip', type=str,
                        help='exclude ip address',
                        required=True)
    parser.add_argument('-r', '--router-ip', type=str,
                        help='ip address of home router',
                        default='192.168.1.1')
    parser.add_argument('-d', '--video-dev', type=str,
                        help='video device path (ex. /dev/video2)',
                        required=True)
    parser.add_argument('-a', '--audio-idx', type=str,
                        help='audio device index (ex. pactl list)',
                        required=True)

    ARGS, _ = parser.parse_known_args()
    main(_)

