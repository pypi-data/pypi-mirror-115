# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 17:29
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : Ethernet.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

import re
from .base import ProtocolBase


class Ethernet(ProtocolBase):
    PROPERTY = ['src_mac', 'dst_mac', 'cvlan_id', 'cvlan_pri', 'svlan_id', 'next_protocol']
    IGNORE_KEY = ['cvlan_id', 'cvlan_pri', 'svlan_id']

    def __init__(self):
        super().__init__()
        self.min_len = self.real_len = 14
        self.name = 'ETHERNET'
        self.vlan_count = 0

        self.src_mac = None
        self.dst_mac = None
        self.cvlan_id = None
        self.cvlan_pri = None
        self.svlan_id = None
        self.next_protocol = None

    def hname(self):
        res = ['ETHERNET']
        for i in range(self.vlan_count):
            res.append('VLAN')
        return res

    def set_property(self, src_mac: str = None, dst_mac: str = None, cvlan_id: int = None, cvlan_pri: int = None,
                     svlan_id: int = None, next_protocol: str = None):
        """

        :param src_mac: 源 MAC 地址。
        :param dst_mac: 目的 MAC 地址。
        :param cvlan_id: 私网 VLAN ID
        :param cvlan_pri: 私网 VLAN 优先级
        :param svlan_id: 运营商分配给用户的公网 VLAN ID
        :param next_protocol: 表示帧类型。取值为 0x8100 时表示 802.1Q Tag 帧。
                    如果不支持 802.1Q的设备收到这样的帧，会将其丢弃。
        """
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.cvlan_id = cvlan_id
        self.cvlan_pri = cvlan_pri
        self.svlan_id = svlan_id
        self.next_protocol = next_protocol

    def _get_protocol_code(self, protocol):
        code_map = {
            'IPV4': '0800',
            'IPV6': '0800',
            'VLAN': '8100'
        }
        return code_map.get(protocol.upper(), '0000')

    def _get_protocol_by_code(self, code):
        code_map = {
            '0800': 'IP',
            '8100': 'VLAN'
        }
        protocol = code_map.get(code)
        if not protocol:
            raise Exception(f'Unexpected protocol code：{code}')
        return protocol

    def _get_header(self):
        next_protocol = self._get_protocol_code(self.next_protocol)
        # 获取VLAN头
        vlan_header = ''
        # 双层VLAN
        if self.cvlan_id and self.svlan_id:
            # 获取外层VLAN头
            vlan_header += self.get_vlan_part(vid=self.svlan_id)
            # 获取内层层VLAN头
            vlan_header += self.get_vlan_part(pri=self.cvlan_pri, vid=self.cvlan_id)
        elif self.cvlan_id and self.svlan_id == None:
            vlan_header += self.get_vlan_part(pri=self.cvlan_pri, vid=self.cvlan_id)
        elif self.cvlan_id == None and self.svlan_id:
            vlan_header += self.get_vlan_part(vid=self.svlan_id)
        ethernet_header = self.add_str(self.dst_mac.replace(':', ''), self.src_mac.replace(':', ''), vlan_header,
                                       next_protocol)
        print(f'ethernet_header:{ethernet_header}')
        return ethernet_header

    def get_vlan_part(self, pri: int = 0, cfi: str = '0', vid: int = 100, type='8100'):
        """

        :param pri: Priority，长度为 3 比特，表示帧的优先级，取值范围为 0～7，值越大优先级越高。
                    用于当阻塞时，优先发送优先级高的数据包。如果设置用户优先级，但是没有 VLANID，
                    则 VLANID 必须设置为 0x000。
        :param cfi: CFI (Canonical Format Indicator)，长度为 1 比特，表示 MAC 地址是否是经典格式。
                    CFI 为 0 说明是标准格式，CFI 为 1 表示为非标准格式。用于区分以太网帧、FDDI（Fiber
                    Distributed Digital Interface）帧和令牌环网帧。在以太网中，CFI 的值为 0。
        :param vid: LAN ID，长度为 12 比特，表示该帧所属的 VLAN。在 VRP 中，可配置的 VLAN ID 取值范
                    围为 1～4094。0 和 4095 协议中规定为保留的 VLAN ID。
                    三种类型：
                        Untagged 帧：VID 不计
                        Priority-tagged 帧：VID 为 0x000
                        VLAN-tagged 帧：VID 范围 0～4095
                    三个特殊的 VID：  0x000：设置优先级但无 VID
                        0x001：缺省 VID
                        0xFFF：预留 VID
        :param type:表示帧类型。取值为 0x8100 时表示 802.1Q Tag 帧。如果不支持 802.1Q
                    的设备收到这样的帧，会将其丢弃。
        :return:
        """
        vlan_header = type + self.bin2hex(str(bin(pri)).lstrip('0b') + str(cfi) + str(bin(vid)).lstrip('0b').zfill(12),
                                          4)
        print(f'vlan_header:{vlan_header}')
        self.vlan_count += 1
        return vlan_header

    def _exec_format(self, header, **kwargs):
        vlan_count = kwargs.get('vlan_count')
        self.src_mac = ':'.join(re.findall(r'.{2}', header[0:12]))
        self.dst_mac = ':'.join(re.findall(r'.{2}', header[12:24]))
        if vlan_count == 0:
            next_protocol = self._get_protocol_by_code(header[24:28])
            remain_header = header[28:]
        elif vlan_count == 1:
            next_protocol = self._get_protocol_by_code(header[32:36])
            remain_header = header[36:]
            vlan = header[24:32]
            qos = self.hex2bin(vlan[4:8], 16)
            self.svlan_id = int(qos[4:16], 2)
        elif vlan_count == 2:
            next_protocol = self._get_protocol_by_code(header[40:44])
            remain_header = header[44:]
            vlan1 = header[24:32]
            qos1 = self.hex2bin(vlan1[4:8], 16)
            self.svlan_id = int(qos1[4:16], 2)
            vlan2 = header[32:40]
            qos2 = self.hex2bin(vlan2[4:8], 16)
            self.cvlan_pri = int(qos2[0:3], 2)
            self.cvlan_id = int(qos2[4:16], 2)
        else:
            raise ValueError('')

        self.next_protocol = next_protocol
        return self.property, remain_header
