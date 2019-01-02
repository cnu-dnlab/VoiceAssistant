import datetime
import cv2
import subprocess

from vapm_collector_interface import VAPMInterface

class VAPMCollectorCamera(VAPMInterface):
    def __init__(self, tmp_path, camera_number=0):
        super().__init__(tmp_path)
        self.capture = cv2.VideoCapture(camera_number)
        self.frame_size = [640, 480]
        # video frame setting
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
        # select codec
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
    def _do_collect(self):
        self.video = cv2.VideoWriter(self.tmp_filepath, self.fourcc, 30.0, \
                                    (self.frame_size[0], self.frame_size[1]))
        while True:
            ret, frame = self.capture.read()
            # show frame to display
            cv2.imshow("VideoFrame", frame)
            self.video.write(frame)
            # if press any key, break
            if cv2.waitKey(1) > 0: break
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
                        default=0,
                        required=True)
    parser.add_argument('-o', '--output',
                        help='output file path',
                        type=str,
                        required=True)
    ARGS = parser.parse_args()

    vapm_camera = VAPMCollectorCamera(ARGS.tmp_path, ARGS.device)
    vapm_camera.start_collect(ARGS.output)
