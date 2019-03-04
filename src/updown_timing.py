import csv
from operator import itemgetter


IP_PROTO = {'6': 'TCP',
            '17': 'UDP'}


class UpDownTiming(object):
    def __init__(self, csv_path):
        self.updown = dict()
        self.dns = dict()
        self.csv_path = csv_path
        self.host_ip = self._get_host_ip()

    def _get_host_ip(self):
        ip_counter = dict()
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                src_ip = row['ip.src']
                dst_ip = row['ip.dst']
                ip_counter[src_ip] = ip_counter.get(src_ip, 0) + 1
                ip_counter[dst_ip] = ip_counter.get(dst_ip, 0) + 1
        return max(ip_counter.items(), key=itemgetter(1))[0]

    def get_updown_timing(self):
        if len(self.updown) > 0:
            return self.updown
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    proto = row['ip.proto']
                    src_ip = row['ip.src']
                    dst_ip = row['ip.dst']
                    if src_ip != self.host_ip and dst_ip != self.host_ip:
                        continue
                    if IP_PROTO[proto] == 'UDP':
                        self._update_udp(row)
                    elif IP_PROTO[proto] == 'TCP':
                        self._update_tcp(row)
                except KeyError:  # packet without ip.proto ex.mdns
                    continue
            
            rdns = self._get_rdns()
            for key in self.updown.keys():
                item = self.updown[key]
                ip = key.split(':')[0]
                if ip not in rdns.keys():
                    continue
                if 'start' in rdns[ip]:
                    item.append((rdns[ip]['start'], 'dns'))
                if 'end' in rdns[ip]:
                    item.append((rdns[ip]['end'], 'dns'))
                self.updown[key] = item

        return self.updown, rdns

    def _update_udp(self, row):
        time_relative = row['frame.time_relative']
        src_ip = row['ip.src']
        src_port = row['udp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['udp.dstport']
        if src_port == '53' or dst_port == '53':
            return self._update_dns(row)
        udp_key = self._get_udp_key(row)
        item = self.updown.get(udp_key, list())
        if int(row['udp.length']) < 1:
            return
        if src_ip == self.host_ip:
            data = str(int(row['udp.length']))
        else:
            data = str(-int(row['udp.length']))
        item.append((time_relative, data))
        self.updown[udp_key] = item

    def _update_dns(self, row):
        time_relative = row['frame.time_relative']
        src_ip = row['ip.src']
        src_port = row['udp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['udp.dstport']
        qry_name = row['dns.qry.name']
        if qry_name not in self.dns.keys():
            self.dns[qry_name] = dict()
        if dst_port == '53':
            self.dns[qry_name]['start'] = time_relative
        elif src_port == '53':
            aname = row['dns.a']
            self.dns[qry_name]['end'] = time_relative
            self.dns[qry_name]['aname'] = aname.split(',')

    def _get_udp_key(self, row):
        src_ip = row['ip.src']
        src_port = row['udp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['udp.dstport']
        if src_ip != self.host_ip:
            return '{0}:{1}-{2}'.format(src_ip, src_port, dst_port)
        else:
            return '{0}:{1}-{2}'.format(dst_ip, dst_port, src_port)

    def _update_tcp(self, row):
        time_relative = row['frame.time_relative']
        src_ip = row['ip.src']
        src_port = row['tcp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['tcp.dstport']
        tcp_key = self._get_tcp_key(row)
        syn = row['tcp.flags.syn']
        fin = row['tcp.flags.fin']
        ssl = row['ssl.handshake']
        item = self.updown.get(tcp_key, list())
        if syn == '1':
            data = 'syn'
        elif fin == '1':
            data = 'fin'
        elif ssl == '1':
            data = 'ssl'
        else:
            if int(row['tcp.len']) < 1:
                data = 0
            elif src_ip == self.host_ip:
                data = str(int(row['tcp.len']))
            else:
                data = str(-int(row['tcp.len']))
        if data != 0:
            item.append((time_relative, data))
            self.updown[tcp_key] = item

    def _get_tcp_key(self, row):
        src_ip = row['ip.src']
        src_port = row['tcp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['tcp.dstport']
        if src_ip != self.host_ip:
            return '{0}:{1}-{2}'.format(src_ip, src_port, dst_port)
        else:
            return '{0}:{1}-{2}'.format(dst_ip, dst_port, src_port)

    def _get_rdns(self):
        rdns = dict()
        for key in self.dns.keys():
            item = self.dns[key]
            if 'aname' not in item.keys():
                continue
            for aname in item['aname']:
                if aname not in rdns.keys():
                    rdns[aname] = dict()
                    rdns[aname]['url'] = key
                if 'start' in item.keys():
                    rdns[aname]['start'] = item['start']
                if 'end' in item.keys():
                    rdns[aname]['end'] = item['end']
        return rdns
