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
        ## Start collector

        ## Play scenario
        cpath = '-'.join([dev, cat, com])
        data = {'dev': dev, 'cat': cat, 'com': com, 
                'mroot': mroot, 'cpath': cpath}
        scene = get_scenario(sroot, sce)
        play_scenario(scene, data)

        ## Stop collector and archive data

    """Refactoring...
    1. Find method to control tcpdump process on router
         include send SIGINT to it
    """


"""
    pcap_process = subprocess.Popen('python3 ./src/vapm_collector_pcap.py -t {0} -r {1} -o {2}'.format(
        os.path.join(ARGS.tmp_dir, 'vapm.pcap'),
        ARGS.router_ip,
        os.path.join(ARGS.output, 'vapm.pcap')).split(' '))
    recorder_process = subprocess.Popen('python3 ./src/vapm_collector_recorder.py -t {0} -o {1}'.format(
        os.path.join(ARGS.tmp_dir, 'vapm.wav'),
        os.path.join(ARGS.output, 'vapm.wav')).split(' '))
    camera_process = subprocess.Popen('python3 ./src/vapm_collector_camera.py -t {0} -o {1}'.format(
        os.path.join(ARGS.tmp_dir, 'vapm.mp4'),
        os.path.join(ARGS.output, 'vapm.mp4')).split(' '))

    try:
        while True:
            time.sleep(10)
            print('Taking...')
    except KeyboardInterrupt:
        print('Stop taking...')
        pcap_process.send_signal(signal.SIGINT)
        recorder_process.send_signal(signal.SIGINT)
        camera_process.send_signal(signal.SIGINT)
"""


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
    parser.add_argument('-r', '--router-ip', type=str,
                        help='ip address of home router',
                        default='192.168.1.1')

    ARGS, _ = parser.parse_known_args()
    main(_)


#    croot = os.path.abspath(os.path.expanduser(CONFIG['Collector']['Path']))
#    cpcap = os.path.join(croot, 'vapm_collector_pcap.py')
#    cmp4 = os.path.join(croot, 'vapm_collector_mp4.py')
    
    
#    cmd = 'python3 {0} -t /tmp/vapm.pcap -r 192.168.1.1 -o ./ -e 192.168.1.127'.format(cpcap)
#    pcap = subprocess.Popen(shlex.split(cmd))
#    print(pcap)
#    time.sleep(10)
#    pcap.send_signal(signal.SIGINT)
    
    ## chdir to file located directory 
    #os.chdir(os.path.dirname(os.path.abspath(__file__)))
"""    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--tmp-dir',
                        help='tmp file directory',
                        type=str,
                        required=True)
    arg_parser.add_argument('-o', '--output',
                        help='output file directory',
                        type=str,
                        required=True)
    arg_parser.add_argument('-r', '--router-ip',
                        help='ip address of home router',
                        type=str,
                        default='192.168.1.1')
    ARGS = parser.parse_args()
    main()
"""

