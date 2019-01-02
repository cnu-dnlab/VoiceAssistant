
import os
import queue
import shutil


import sounddevice as sd
import soundfile as sf

import numpy



from vapm_collector_interface import VAPMInterface


class VAPMCollectorRecorder(VAPMInterface):
    FILE_NAME = 'sound'
    EXTENSION_WAV = '.wav'
    STORE_PATH = './tmp/recorder/'

    def __init__(self, tmp_path, channels, device, samplerate):
        super().__init__(tmp_path)
        self.file_wav = tmp_path

        self.queue_for_store = queue.Queue()

        self.channel = channels
        self.device = device
        self.sample_rate = samplerate


    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.queue_for_store.put(indata.copy())

    def archive_tmp(self, target):
        print("\n\n Record End:"+repr(self.file_wav))
        target_filepath = os.path.abspath(target)
        shutil.copyfile(self.tmp_filepath, target_filepath)

    def _do_collect(self):
        with sf.SoundFile(self.file_wav, mode='x', samplerate=self.sample_rate,
                          channels=self.channel, subtype=None) as save_file, sd.InputStream(
                              samplerate=self.sample_rate, device=self.device,
                              channels=self.channel, callback=self.callback):
            print('recording ... ')
            while True:
                save_file.write(self.queue_for_store.get())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-t', '--tmp-path', type=str,
        default='./tmp/recorder/sound.wav',
        help='tmp file location',
    )

    parser.add_argument(
        '-d', '--device', type=int, default=None,
        help='input device (number ID)'
    )
    parser.add_argument(
        '-r', '--samplerate', type=int, default=44100,
        help='input sample rate for recording'
    )
    parser.add_argument(
        '-c', '--channels', type=int, default=2,
        help='input channels'
    )
    parser.add_argument(
        '-o', '--output', type=str,
        default='./temp.wav',
        help='ouput file path'
    )
    ARGS = parser.parse_args()

    vapm_recorder = VAPMCollectorRecorder(
        ARGS.tmp_path, ARGS.channels, ARGS.device, ARGS.samplerate
        )

    vapm_recorder.start_collect(ARGS.output)
