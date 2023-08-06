# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 17:30
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : TCP.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

from .base import ProtocolBase


class Tcp(ProtocolBase):
    PROPERTY = ['tcp_src_port', 'tcp_dst_port', 'seq_num', 'ack_num', 'header_len', 'reserved', 'flag_urg', 'flag_ack',
                'flag_psh', 'flag_rst', 'flag_syn', 'flag_fin', 'window', 'checksum', 'urgent']
    IGNORE_KEY = ['seq_num', 'ack_num', 'header_len', 'reserved', 'flag_urg', 'flag_ack', 'flag_psh', 'flag_rst',
                  'flag_syn', 'flag_fin', 'window', 'checksum', 'urgent']

    def __init__(self):
        super().__init__()
        self.min_len = self.real_len = 20
        self.name = 'TCP'

        self.tcp_src_port = None
        self.tcp_dst_port = None
        self.seq_num = None
        self.ack_num = None
        self.header_len = None
        self.reserved = None
        self.flag_urg = None
        self.flag_ack = None
        self.flag_psh = None
        self.flag_rst = None
        self.flag_syn = None
        self.flag_fin = None
        self.window = None
        self.checksum = None
        self.urgent = None

    def hname(self):
        return ['TCPCHECK']

    def set_property(self, tcp_src_port: int = None, tcp_dst_port: int = None, seq_num: int = 0, ack_num: int = 0,
                     header_len: int = 5, flag_urg: int = 0, flag_ack: int = 1, flag_psh: int = 0, flag_rst: int = 0,
                     flag_syn: int = 0, flag_fin: int = 0, window: int = 4096, checksum: int = 0, urgent: int = 0):
        """

        :param tcp_src_port: 16 比特的源端口其中包含初始化通信的端口。源端口和源IP地址的作用是标示报问的返回地址。
        :param tcp_dst_port: 16 比特的目的端口域定义传输的目的。这个端口指明报文接收计算机上的应用程序地址接口。
        :param seq_num: 32 比特 序号字段。TCP 链接中传输的数据流中每个字节都编上一个序号。
                        序号字段的值指的是本报文段所发送的数据的第一个字节的序号。
        :param ack_num: 32 比特 确认号，是期望收到对方的下一个报文段的数据的第 1 个字节的序号，即上次已成功接
                        收到的数据字节序号加 1。只有 ACK 标识为 1，此字段有效。
        :param header_len: 4 比特 数据偏移，即首部长度，指出 TCP 报文段的数据起始处距离 TCP 报文段的起始处有多远，
                            以 32 比特（4 字节）为计算单位。最多有 60 字节的首部，若无选项字段，正常为 20字节。
        :param reserved: 6 比特 保留，必须填 0。
        :param flag_urg: 1 比特 紧急指针标志，为1时表示紧急指针有效，为0则忽略紧急指针。
        :param flag_ack: 1 比特 确认序号标志，为1时表示确认号有效，为0表示报文中不含确认信息，忽略确认号字段。
        :param flag_psh: 1 比特 push标志，为1表示是带有push标志的数据，指示接收方在接收到该报文段以后，
                        应尽快将这个报文段交给应用程序，而不是在缓冲区排队。
        :param flag_rst: 1 比特 重置连接标志，用于重置由于主机崩溃或其他原因而出现错误的连接。或者用于拒绝非法的报文段和拒绝连接请求。
        :param flag_syn: 1 比特 同步序号，用于建立连接过程，在连接请求中，SYN=1和ACK=0表示该数据段没有使用捎带的确认域，
                        而连接应答捎带一个确认，即SYN=1和ACK=1。
        :param flag_fin: 1 比特 finish标志，用于释放连接，为1时表示发送方已经没有数据发送了，即关闭本方数据流。
        :param window: 16 比特 滑动窗口大小，用来告知发送端接受端的缓存大小，以此控制发送端发送数据的速率，从而达到流量控制。
                        窗口大小时一个16bit字段，因而窗口大小最大为65535。
        :param checksum: 16 比特 奇偶校验，此校验和是对整个的 TCP 报文段，包括 TCP 头部和 TCP 数据，以 16 位字进行计算所得。
                        由发送端计算和存储，并由接收端进行验证。
        :param urgent: 16 比特 只有当 URG 标志置 1 时紧急指针才有效。紧急指针是一个正的偏移量，和顺序号字段中的值相加表示紧急
                        数据最后一个字节的序号。 TCP 的紧急方式是发送端向另一端发送紧急数据的一种方式。
        """
        self.tcp_src_port = tcp_src_port
        self.tcp_dst_port = tcp_dst_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.header_len = header_len
        self.reserved = '000000'
        self.flag_urg = flag_urg
        self.flag_ack = flag_ack
        self.flag_psh = flag_psh
        self.flag_rst = flag_rst
        self.flag_syn = flag_syn
        self.flag_fin = flag_fin
        self.window = window
        self.checksum = checksum
        self.urgent = urgent

    def _get_header(self):
        # 源端口
        tcp_src_port = self.int2hex(self.tcp_src_port, 4)
        # 目的端口
        tcp_dst_port = self.int2hex(self.tcp_dst_port, 4)
        # 序号
        seq_num = self.int2hex(self.seq_num, 8)
        # 确认号
        ack_num = self.int2hex(self.ack_num, 8)
        # 数据偏移、首部长度、保留、控制位
        df = self.bin2hex(
            self.int2bin(self.header_len, 4) + self.reserved + str(self.flag_urg) + str(self.flag_ack) + str(
                self.flag_psh) + str(self.flag_rst) + str(self.flag_syn) + str(self.flag_fin), 4)
        # 窗口
        window = self.int2hex(self.window, 4)
        # 校验和
        checksum = self.int2hex(self.checksum, 4)
        # 紧急指针
        urgent = self.int2hex(self.urgent, 4)
        tcp_header = self.add_str(tcp_src_port, tcp_dst_port, seq_num, ack_num, df, window, checksum, urgent)
        print(f'tcp_header:{tcp_header}')
        return tcp_header

    def _exec_format(self, header, **kwargs):
        tcp = header[0:40]
        remain_header = header[40:]
        self.tcp_src_port = int(tcp[0:4], 16)
        self.tcp_dst_port = int(tcp[4:8], 16)
        self.seq_num = int(tcp[8:16], 16)
        self.ack_num = int(tcp[16:24], 16)
        drf = self.hex2bin(tcp[24:28], 16)
        self.header_len = int(drf[0:4], 2)
        self.reserved = '000000'
        self.flag_urg = int(drf[10])
        self.flag_ack = int(drf[11])
        self.flag_psh = int(drf[12])
        self.flag_rst = int(drf[13])
        self.flag_syn = int(drf[14])
        self.flag_fin = int(drf[15])
        self.window = int(tcp[28:32], 16)
        self.checksum = int(tcp[32:36], 16)
        self.urgent = int(tcp[36:40], 16)

        return self.property, remain_header
