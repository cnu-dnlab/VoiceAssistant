import datetime
import cv2
import subprocess

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
        
    def _do_collect(self):
        self.video = cv2.VideoWriter(self.tmp_filepath, self.fourcc, 30.0,\
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
    vapm_camera = VAPMCollectorCamera('./tmp/camera/webcam.mp4', 0)
    vapm_camera.start_collect('./temp.mp4')