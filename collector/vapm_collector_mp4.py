import sys
import subprocess
import shlex
import threading
import signal
import re

from vapm_collector_interface import VAPMInterface

ARGS = None


def signal_handler(signal, frame):
    print(signal, frame)



class VAPMCollectorMP4(VAPMInterface):
    def __init__(self, tmp_path, video_dev, audio_idx):
        super().__init__(tmp_path)
        self.video_dev = video_dev
        self.audio_idx = audio_idx

    def start_collect(self, target):  # override
        self.clear_tmp()
        self._do_collect()
        self._stop_collect()
        self.archive_tmp(target)
        self.clear_tmp()

    def _do_collect(self):  # override
        cmd = ('guvcview -d {0} -a pulse -k {1} -e -j {2}').format(
                 self.video_dev, self.audio_idx, self.tmp_filepath)
        self.proc = subprocess.Popen(cmd, shell=True,
                         start_new_session=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        import time
        time.sleep(2)
        cmd = ('killall -USR1 guvcview')
        subprocess.run(cmd, shell=True)
        while True:
            try:
                self.proc.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                pass
            except KeyboardInterrupt:
                break

    def _stop_collect(self):  # override
        cmd = ('killall -USR1 guvcview')
        subprocess.run(cmd, shell=True)
        cmd = ('killall -SIGINT guvcview')
        subprocess.run(cmd, shell=True)
        stdout = self.proc.stdout.read().decode('utf-8')
        self.tmp_filepath = re.findall(
          r'saving video to ([\w/.-]+)', stdout)[0]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tmp-path',
                        help='tmp file location',
                        type=str,
                        required=True)
    parser.add_argument('-d', '--video_dev',
                        help='video device',
                        type=str,
                        required=True)
    parser.add_argument('-i', '--audio_idx',
                        help='audio device index',
                        type=str,
                        required=True)
    parser.add_argument('-o', '--output',
                        help='output file path',
                        type=str,
                        required=True)
    ARGS = parser.parse_args()
                        
    vapm_mp4 = VAPMCollectorMP4(ARGS.tmp_path, 
                                  ARGS.video_dev, ARGS.audio_idx)
    vapm_mp4.start_collect(ARGS.output)

