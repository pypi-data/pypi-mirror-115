# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/8/5 9:29
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : pkt.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/8/5 : create new
# ----------------------------------------------------------------

import dpkt
import socket
from dpkt.compat import compat_ord


def byte2hex(bstr):
    return bytes(bstr).decode('ascii')


def hex2byte(hstr):
    return bytes().fromhex(hstr)


def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)


class DealPkt(object):
    def __init__(self):
        self.pkt_property = {}

    def pack_ethernet(self):
        pass

    def extract(self, buf, protocol=None):
        if not isinstance(buf, bytes) and isinstance(buf, str):
            buf = bytes().fromhex(buf)
        ext_data = {}
        data = _protocol = None
        if protocol == 'ethernet':
            _protocol = 'ethernet'
            eth = dpkt.ethernet.Ethernet(buf)
            ext_data['src_mac'] = mac_addr(eth.src)
            ext_data['dst_mac'] = mac_addr(eth.dst)
            if hasattr(eth, 'vlan_tags'):
                vlans = []
                vlan_tags = eth.vlan_tags
                for vlan in vlan_tags:
                    vlan_info = {}
                    vlan_info['pri'] = vlan.pri
                    vlan_info['cfi'] = vlan.cfi
                    vlan_info['id'] = vlan.id
                    vlans.append(vlan_info)
                ext_data['vlans'] = vlans
            data = eth.data
        elif protocol == 'ipv4' or isinstance(buf, dpkt.ip.IP):
            ip = buf
            _protocol = 'ipv4'
            ext_data['src_ip'] = inet_to_str(ip.src)
            ext_data['dst_ip'] = inet_to_str(ip.dst)
            ext_data['v'] = ip.v
            ext_data['hl'] = ip.hl
            ext_data['len'] = ip.len
            ext_data['tos'] = ip.tos
            ext_data['id'] = ip.id
            ext_data['p'] = ip.p
            ext_data['ttl'] = ip.ttl
            ext_data['DF'] = bool(ip.off & dpkt.ip.IP_DF)
            ext_data['mf'] = bool(ip.off & dpkt.ip.IP_MF)
            ext_data['offset'] = ip.off & dpkt.ip.IP_OFFMASK
            data = ip.data
        elif protocol == 'tcp' or isinstance(buf, dpkt.tcp.TCP):
            tcp = buf
            _protocol = 'tcp'
            ext_data['tcp_src_port'] = tcp.sport
            ext_data['tcp_dst_port'] = tcp.dport
            ext_data['seq'] = tcp.seq
            ext_data['ack'] = tcp.ack
            ext_data['off'] = tcp.off
            ext_data['flags'] = tcp.flags
            ext_data['win'] = tcp.win
            ext_data['sum'] = tcp.sum
            ext_data['urp'] = tcp.urp
            data = tcp.data
        elif protocol == 'udp' or isinstance(buf, dpkt.udp.UDP):
            udp = buf
            _protocol = 'udp'
            ext_data['udp_src_port'] = udp.sport
            ext_data['udp_dst_port'] = udp.dport
            ext_data['ulen'] = udp.ulen
            ext_data['sum'] = udp.sum
            data = udp.data
        else:
            pass
        return ext_data, data, _protocol

    def unpack(self, buf, l2=None):
        protocol = ext_data = data = None
        if l2 == 'ethernet':
            ext_data, data, protocol = self.extract(buf, 'ethernet')
        else:
            ext_data, data, protocol = self.extract(buf)
        if ext_data:
            self.pkt_property[protocol] = ext_data
        if data:
            self.unpack(data)
        return self.pkt_property
