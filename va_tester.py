import os
import subprocess
import time
import signal

ARGS = None


def main():
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

