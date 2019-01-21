import os
import sys
from multiprocessing import Process

from src.vapm_collector_pcap import VAPMCollectorPcap
from src.vapm_collector_recorder import VAPMCollectorRecorder
from src.vapm_collector_camera import VAPMCollectorCamera

ARGS = None


def main():
    vapm_pcap = VAPMCollectorPcap(os.path.join(ARGS.tmp_dir, 'vapm.pcap'),
                                  ARGS.router_ip)
    vapm_recorder = VAPMCollectorRecorder(os.path.join(ARGS.tmp_dir, 'vapm.wav'),
                                          2, None, 44100)
    vapm_camera = VAPMCollectorCamera(os.path.join(ARGS.tmp_dir, 'vapm.mp4'),
                                      0)
    pcap_process = Process(target=vapm_pcap.start_collect, args=(os.path.join(ARGS.output, 'vapm.pcap'),))
    recorder_process = Process(target=vapm_recorder.start_collect, args=(os.path.join(ARGS.output, 'vapm.wav'),))
    camera_process = Process(target=vapm_camera.start_collect, args=(os.path.join(ARGS.output, 'vapm.mp4'),))
    
    try:
        pcap_process.start()
        recorder_process.start()
        camera_process.start()
    except KeyboardInterrupt:
        pcap_process.terminate()
        recorder_process.terminate()
        camera_process.terminate()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tmp-dir',
                        help='tmp file directory',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output',
                        help='output file directory',
                        type=str,
                        required=True)
    parser.add_argument('-r', '--router-ip',
                        help='ip address of home router',
                        type=str,
                        default='192.168.1.1')
    ARGS = parser.parse_args()
    main()
