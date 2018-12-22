class VAMPInterface(object):
    def __init__(self):
        pass

    def clear_tmp(self):
        pass
    
    def archive_tmp(self):
        pass

    def start_collect(self):
        self.clear_tmp(self):
        try:
            self._do_collect()
        except:
            self.archive_tmp()

    def _do_collect(self):
        raise NotImplementedError
