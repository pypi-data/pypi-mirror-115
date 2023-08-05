# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 17:31
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : UDP.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

from .base import ProtocolBase


class Udp(ProtocolBase):
    PROPERTY = ['udp_src_port', 'udp_dst_port', 'total_len', 'checksum']
    IGNORE_KEY = ['checksum']

    def __init__(self):
        super().__init__()
        self.min_len = self.real_len = 8
        self.name = 'UDP'

    def hname(self):
        return ['UDP']

    def set_property(self, udp_src_port: int = None, udp_dst_port: int = None, total_len: int = None,
                     checksum: int = 0):
        """

        :param tcp_src_port: 16 比特 的源端口其中包含初始化通信的端口。源端口和源IP地址的作用是标示报问的返回地址。
        :param tcp_dst_port: 16 比特 的目的端口域定义传输的目的。这个端口指明报文接收计算机上的应用程序地址接口。
        :param total_len: 16 比特 用户数据报长度：包括报头和数据部分的总长度。
        :param checksum: 16 比特 UDP协议不做错误纠正，发现错误会丢弃掉并发出警告。
                        用于校验UDP数据报的数字段和包含UDP数据报首部的“伪首部”。其校验方法同IP分组首部中的首部校验和。
                        伪首部，又称为伪包头（Pseudo Header）：是指在TCP的分段或UDP的数据报格式中，在数据报
                        首部前面增加源IP地址、目的IP地址、IP分组的协议字段、TCP或UDP数据报的总长度等共12字节，
                        所构成的扩展首部结构。此伪首部是一个临时的结构，它既不向上也不向下传递，仅仅只是为了保证
                        可以校验套接字的正确性。
        """
        self.udp_src_port = udp_src_port
        self.udp_dst_port = udp_dst_port
        self.total_len = total_len
        self.checksum = checksum

    def _get_header(self):
        # 源端口
        udp_src_port = self.int2hex(self.udp_src_port, 4)
        # 目的端口
        udp_dst_port = self.int2hex(self.udp_dst_port, 4)
        # 长度
        if self.total_len == None:
            self.total_len = self.remain_len
        total_len = self.int2hex(self.total_len, 4)
        # 校验和
        checksum = self.int2hex(self.checksum, 4)
        udp_header = self.add_str(udp_src_port, udp_dst_port, total_len, checksum)
        print(f'udp_header:{udp_header}')
        return udp_header

    def _exec_format(self, header, **kwargs):
        udp = header[0:16]
        remain_header = header[40:]
        self.udp_src_port = int(udp[0:4], 16)
        self.udp_dst_port = int(udp[4:8], 16)
        self.total_len = int(udp[8:12], 16)
        self.checksum = int(udp[12:16], 16)
        return self.property, remain_header
