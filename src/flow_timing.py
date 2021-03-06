import csv
from operator import itemgetter


IP_PROTO = {'6': 'TCP',
            '17': 'UDP'}


class FlowTiming(object):
    def __init__(self, csv_path):
        self.flow = dict()
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

    def get_flow_timing(self):
        if len(self.flow) > 0:
            return self.flow
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
        for key in self.flow.keys():
            item = self.flow[key]
            key_ip = key.split(':')[0]
            if key_ip in rdns.keys():
                item['domainLookupStart'] = rdns[key_ip]['domainLookupStart']
                item['domainLookupEnd'] = rdns[key_ip]['domainLookupEnd']
            self.flow[key] = item

        return self.flow

    def _update_udp(self, row):
        time_relative = row['frame.time_relative']
        src_ip = row['ip.src']
        src_port = row['udp.srcport']
        dst_ip = row['ip.dst']
        dst_port = row['udp.dstport']
        qry_name = row['dns.qry.name']
        udp_key = self._get_udp_key(row)
        if qry_name not in self.dns.keys():
            self.dns[qry_name] = dict()
        if dst_port == '53':
            self.dns[qry_name]['domainLookupStart'] = time_relative
        elif src_port == '53':
            aname = row['dns.a']
            self.dns[qry_name]['domainLookupEnd'] = time_relative
            self.dns[qry_name]['aname'] = aname.split(',')
        if src_port == '443' or dst_port == '443':
            item = self.flow.get(udp_key, dict())
            #if 'quicConnectStart' not in item.keys():
            #    item['quickConnectStart'] = time_relative
            #item['quicConnectEnd'] = time_relative
            if src_ip == self.host_ip:
                if 'requestStart' not in item.keys():
                    item['requestStart'] = time_relative
            elif dst_ip == self.host_ip:
                if 'responseStart' not in item.keys():
                    item['responseStart'] = time_relative
                item['responseEnd'] = time_relative
            self.flow[udp_key] = item

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
        syn = row['tcp.flags.syn']
        ack = row['tcp.flags.ack']
        fin = row['tcp.flags.fin']
        push = row['tcp.flags.push']
        ssl = row['ssl.handshake']
        ip_len = int(row['ip.len'])
        tcp_key = self._get_tcp_key(row)
        item = self.flow.get(tcp_key, dict())

        if syn == '1' and 'connectStart' not in item.keys():
            item['connectStart'] = time_relative
        if fin == '1' and 'connectEnd' not in item.keys():
            item['connectEnd'] = time_relative
        if ssl == '1' and 'secureConnectionStart' not in item.keys():
            item['secureConnectionStart'] = time_relative

        if (tcp_key.split(':')[1]).split('-')[0] != '443':
            if 'connectStart' in item.keys():
                if 'requestStart' not in item.keys():
                    if ((ip_len > 100 and src_ip == self.host_ip) or
                        (push == '1' and src_ip == self.host_ip)):
                        item['requestStart'] = time_relative
                else:
                    if 'responseStart' not in item.keys():
                        if ((ip_len > 100 and src_ip != self.host_ip) or
                            (push == '1' and src_ip != self.host_ip)):
                            item['responseStart'] = time_relative
                    else:
                        if ((ip_len > 100 and src_ip != self.host_ip) or
                            (push == '1' and src_ip != self.host_ip)):
                            item['responseEnd'] = time_relative
            else:
                if 'requestStart' not in item.keys():
                    if ((ip_len > 100 and src_ip == self.host_ip) or
                        (push == '1' and src_ip == self.host_ip)):
                        item['requestStart'] = time_relative
                elif 'responseStart' not in item.keys():
                    if ((ip_len > 100 and src_ip != self.host_ip) or
                        (push == '1' and src_ip != self.host_ip)):
                        item['responseStart'] = time_relative
                else:
                    if ((ip_len > 100 and src_ip != self.host_ip) or
                        (push == '1' and src_ip != self.host_ip)):
                        item['responseEnd'] = time_relative
        elif (tcp_key.split(':')[1]).split('-')[0] == '443':
            if 'connectStart' in item.keys():
                if ('secureConnectionStart' in item.keys() and
                        'requestStart' not in item.keys()):
                    if ((ip_len > 100 and src_ip == self.host_ip) or
                        (push == '1' and src_ip == self.host_ip)):
                        item['requestStart'] = time_relative
                elif 'secureConnectionStart' in item.keys():
                    if 'responseStart' not in item.keys():
                        if ((ip_len > 100 and src_ip != self.host_ip) or
                            (push == '1' and src_ip != self.host_ip)):
                            item['responseStart'] = time_relative
                    else:
                        if ((ip_len > 100 and src_ip != self.host_ip) or
                            (push == '1' and src_ip != self.host_ip)):
                            item['responseEnd'] = time_relative
            else:
                if 'requestStart' not in item.keys():
                    if ((ip_len > 100 and src_ip == self.host_ip) or
                        (push == '1' and src_ip == self.host_ip)):
                        item['requestStart'] = time_relative
                elif 'responseStart' not in item.keys():
                    if ((ip_len > 100 and src_ip != self.host_ip) or
                        (push == '1' and src_ip != self.host_ip)):
                        item['responseStart'] = time_relative
                else:
                    if ((ip_len > 100 and src_ip != self.host_ip) or
                        (push == '1' and src_ip != self.host_ip)):
                        item['responseEnd'] = time_relative
        self.flow[tcp_key] = item

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
                try:
                    rdns[aname] = {
                        'domainLookupStart': item['domainLookupStart'],
                        'domainLookupEnd': item['domainLookupEnd']}
                except KeyError:
                    continue

        return rdns
