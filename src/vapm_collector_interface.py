import os
import shutil


class VAPMInterface(object):
    def __init__(self, tmp_path):
        self.tmp_filepath = os.path.abspath(tmp_path)
        self._create_tmp_dir()
    
    def _create_tmp_dir(self):
        os.makedirs(os.path.dirname(self.tmp_filepath), exist_ok=True)

    def clear_tmp(self):
        if os.path.exists(self.tmp_filepath):
            os.remove(self.tmp_filepath)
    
    def archive_tmp(self, target):
        target_filepath = os.path.abspath(target)
        shutil.copyfile(self.tmp_filepath, target_filepath)

    def start_collect(self, target):
        self.clear_tmp()
        try:
            self._do_collect()
        except KeyboardInterrupt:
            self.archive_tmp(target)
        self.clear_tmp()

    def _do_collect(self):
        raise NotImplementedError
