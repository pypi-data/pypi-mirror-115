# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 17:30
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : IPV4.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

import re
from .base import ProtocolBase


class Ipv4(ProtocolBase):
    PROPERTY = ['src_ip', 'dst_ip', 'total_len', 'next_protocol', 'version', 'ihl', 'identification', 'flag_mf',
                'flag_df', 'fragment_offset', 'ttl', 'header_checksum', 'ip_pri', 'service_type', 'cu', 'dscp',
                'ipv4_gateway']
    IGNORE_KEY = ['version', 'ihl', 'identification', 'flag_mf', 'flag_df', 'fragment_offset', 'ttl',
                  'header_checksum', 'ip_pri', 'service_type', 'cu', 'dscp', 'ipv4_gateway']

    def __init__(self):
        super().__init__()
        self.min_len = self.real_len = 20
        self.name = 'IPV4'

        self.version = None
        self.ihl = None
        self.total_len = None
        self.identification = None
        self.flag_mf = None
        self.flag_df = None
        self.fragment_offset = None
        self.ttl = None
        self.next_protocol = None
        self.header_checksum = None
        self.src_ip = None
        self.dst_ip = None
        self.ip_pri = None
        self.service_type = None
        self.cu = None
        self.dscp = None
        self.ipv4_gateway = None

    def hname(self):
        return ['IP']

    def _get_protocol_code(self, protocol):
        code_map = {
            'UDP': '11',
            'TCP': '06'
        }
        return code_map.get(protocol.upper(), '00')

    def set_property(self, src_ip: str = None, dst_ip: str = None, version: int = 4, ihl: int = 5,
                     total_len: int = None, identification: str = '0000', flag_mf: int = 0,
                     flag_df: int = 0, fragment_offset: int = 0, ttl: int = 255, next_protocol: str = None,
                     header_checksum: str = '2048',
                     ip_pri: int = 0, service_type: int = 0, cu: str = 0, dscp: int = None, ipv4_gateway: str = None):
        """
            IP优先级==============》3层IP包头的服务类型之一,它由IP分组报头中的服务类型（ToS）字节中的3位组成，
            其在字节中的位置如下：
        　　P2 P1 P0 T3 T2 T1 T0 CU其中：IP优先级：3bit（P2-P0）服务类型（ToS）：4bit（T3-T0）未用（CU）：1bit
        　　IP优先级值有8个（0-7），0优先级最低，7优先级最高。在默认情况下，IP优先级6和7用于网络控制通讯使用，
            不推荐用户使用。ToS字段的服务类型未能在现有的IP网络中普及使用。

            DSCP优先级==============》3层IP包头的服务类型之二,它由IP分组报头中的6位组成，使用的是ToS字节，因此在使用DSCP后，
            该字节也被称为DSCP字节。其在字节中的位置如下：
            DS5 DS4 DS3 DS2 DS1 DS0 CU CU 其中：DSCP优先级：6bit（DS5-DS0）未用（CU）：2bit
            DSCP优先级值有64个（0-63），0优先级最低，63优先级最高。事实上DSCP字段是IP优先级字段的超集，
            DSCP字段的定义向后与IP优先级字段兼容。目前定义的DSCP有默认的DSCP，值为0；类选择器DSCP，
            定义为向后与IP优先级兼容，值为（8，16，24，32，40，48，56）；加速转发（EF），一般用于低延迟的服务，
            推荐值为46（101110）；确定转发（AF），定义了4个服务等级，每个服务等级有3个下降过程，
            因此使用了12个DSCP值（（10，12，14），（18，20，22），（26，28，30），（34，36，38））。

        :param src_ip: 32 bits，指明了发送节点的IP地址。
        :param dst_ip: 32 bits，指明了接收节点的IP地址。
        :param version:  4 bits，显示当前正在运行的IP版本信息。当前为4
        :param ihl: 4 bits，标明了以32比特为单位的消息中数据报报头的长度，这是所有报头的总长度。注意：它的最小值为5
        :param total_len: 16 bits，标明整个分组的长度，以字节为单位。总长度减去IHL就是数据有效载荷的长度。
                        理论上最大长度可以为65535，但报文经过数据链路层时很可能被分片。
        :param identification: 16 bits，包含一个整数，用来标识当前的数据报。这是一个序列号。
        :param flag_mf: 为0 表示该数据段是本分组中最后的一个数据分段,为1  表示后面还有数据分段
        :param flag_df: 为0 表示可以对分组进行分片,为1 表示不可以对分组进行分片
        :param fragment_offset: 13 bits。指示分段在数据包中的位置，用于重组数据分段。这个字段允许标记字段终止在16 Bit的边界
        :param ttl:  8 bits，指示分组在网络传输中的允许保持的时间，以秒为单位。当该计时器为0时，数据报将被丢弃。
        :param next_protocol:  8 bits，指明了在IP处理过程结束后，哪一个上层协议将接收这些数据。
        :param header_checksum: 16 bits，用于确保IP头的完整性。
        :param ip_pri: IP优先级：3bit
        :param service_type: 服务类型（ToS）：4bit
        :param cu: 未用（CU）：1bit
        :param dscp: DSCP优先级：6bit
        """
        self.version = version
        self.ihl = ihl
        self.total_len = total_len
        self.identification = identification
        self.flag_mf = flag_mf
        self.flag_df = flag_df
        self.fragment_offset = fragment_offset
        self.ttl = ttl
        self.next_protocol = next_protocol
        self.header_checksum = header_checksum
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ip_pri = ip_pri
        self.service_type = service_type
        self.cu = cu
        self.dscp = dscp
        self.ipv4_gateway = ipv4_gateway

    def _get_header(self):
        # 版本（Version）
        version = self.int2hex(self.version)
        # 头部长度（Header Length）
        ihl = self.int2hex(int(self.ihl))
        # 区分服务 (Type of Service)
        if self.dscp == None:
            tos = self.bin2hex(self.int2bin(self.ip_pri, 3) + self.int2bin(self.service_type, 4) + str(self.cu), 2)
        else:
            self.cu = '00'
            tos = self.bin2hex(self.int2bin(self.dscp, 6) + str(self.cu), 2)
        # 总长度（Total Length）
        if self.total_len == None:
            self.total_len = self.remain_len
        total_len = self.int2hex(self.total_len, 4)
        # 标识（Identification）
        identification = self.identification
        # 标志（Flags）段偏移（Fragment Offset）
        ff = self.bin2hex('0' + str(self.flag_df) + str(self.flag_mf) + self.int2bin(self.fragment_offset, 13), 4)
        # 生存时间（Time To Live）
        ttl = self.int2hex(self.ttl, 2)
        # 协议（Protocol）
        next_protocol = self._get_protocol_code(self.next_protocol)
        # 校验和（Checksum）
        header_checksum = self.header_checksum
        # 源地址
        src_ip = self.get_hex_ip(self.src_ip)
        # 目的地址
        dst_ip = self.get_hex_ip(self.dst_ip)
        ip_header = self.add_str(version, ihl, tos, total_len, identification, ff, ttl, next_protocol, header_checksum,
                                 src_ip, dst_ip)
        print(f'ip_header:{ip_header}')
        return ip_header

    def _get_protocol_by_code(self, code):
        code_map = {
            '11': 'UDP',
            '06': '11'
        }
        protocol = code_map.get(code)
        if not protocol:
            raise Exception(f'Unexpected protocol code：{code}')
        return protocol

    def _exec_format(self, header, **kwargs):

        ipv4 = header[0:40]
        remain_header = header[40:]
        self.version = int(ipv4[0:1], 16)
        self.ihl = int(ipv4[1:2], 16)
        tos = self.hex2bin(ipv4[2:4], 8)
        self.total_len = int(ipv4[4:8], 16)
        self.identification = ipv4[8:12]
        ff = self.hex2bin(ipv4[12:16], 16)
        self.flag_mf = int(ff[2])
        self.flag_df = int(ff[1])
        self.fragment_offset = int(ff[3:], 2)
        self.ttl = int(ipv4[16:18], 16)
        self.next_protocol = self._get_protocol_by_code(ipv4[18:20])
        self.header_checksum = ipv4[20:24]
        self.src_ip = '.'.join([str(int(x, 16)) for x in re.findall(r'.{2}', ipv4[24:32])])
        self.dst_ip = '.'.join([str(int(x, 16)) for x in re.findall(r'.{2}', ipv4[32:40])])

        return self.property, remain_header
