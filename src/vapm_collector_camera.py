import subprocess

import cv2

from vapm_collector_interface import VAPMInterface


class VAPMCollectorCamera(VAPMInterface):
    def __init__(self, tmp_path, camera_number):
        super().__init__(tmp_path)
        self.capture = cv2.VideoCapture(camera_number)
        self.frame_size = [640, 480]
        # video frame setting
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
        # select codec
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
    def _do_collect(self):  # override
        self.video = cv2.VideoWriter(self.tmp_filepath, self.fourcc, 30.0, \
                                    (self.frame_size[0], self.frame_size[1]))
        while True:
            ret, frame = self.capture.read()
            self.video.write(frame)
        self._stop_collect()

    def _stop_collect(self):  # override
        self.video.release()
        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tmp-path',
                        help='tmp file location',
                        type=str,
                        required=True)
    parser.add_argument('-d', '--device',
                        help='device number of connected camera',
                        type=int,
                        default=0)
    parser.add_argument('-o', '--output',
                        help='output file path',
                        type=str,
                        required=True)
    ARGS = parser.parse_args()

    vapm_camera = VAPMCollectorCamera(ARGS.tmp_path, ARGS.device)
    vapm_camera.start_collect(ARGS.output)

