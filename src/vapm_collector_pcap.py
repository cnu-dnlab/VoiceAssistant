import subprocess

from vapm_collector_interface import VAPMInterface


class VAPMCollectorPcap(VAPMInterface):
    def __init__(self, tmp_path, router_ip):
        super().__init__(tmp_path)
        self.router_ip = router_ip

    def _do_collect(self):  # override
        command = ('ssh root@{0} "tcpdump -i br-lan -s 0 -U -w - '
                   '\(not port 22\)" > {1}').format(self.router_ip,
                                                    self.tmp_filepath)
        self.popen = subprocess.run(command, shell=True)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--tmp_path',
                        help='tmp file location',
                        type=str,
                        required=True)
    parser.add_argument('--router_ip',
                        help='ip address of home router',
                        type=str,
                        required=True)
                        
    vapm_pcap = VAPMCollectorPcap('/tmp/pcap/router.pcap',
                                  '192.168.1.1')
    vapm_pcap.start_collect('./temp.pcap')

