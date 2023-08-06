# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 15:00
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : sock.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : 新增
# ----------------------------------------------------------------

import socket
import sys
import struct
import json
from ..error import SockConnectionError


class SocketDriver(object):

    def __init__(self, hostname, port, timeout=20):
        hostname = hostname.encode()
        self.hostname = hostname
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            # sys.stderr.write("[Socket connection error] Cannot connect to %s, error: %s\n" % (hostname, msg[0]))
            # sys.exit(1)
            raise SockConnectionError(hostname, msg)

        self.sock.settimeout(timeout)

        try:
            self.sock.connect((hostname, port))
        except socket.error as msg:
            # sys.stderr.write("[Socket connection error] Cannot connect to %s, error: %s\n" % (hostname, msg[0]))
            # sys.exit(2)
            raise SockConnectionError(hostname, msg)

    def __del__(self):
        self.sock.close()

    def receive_all(self):
        # 拆包接收
        struct_bytes = self.sock.recv(4)
        header_len = struct.unpack('i', struct_bytes)[0]
        header_bytes = self.sock.recv(header_len)
        header = json.loads(header_bytes.decode())  # 此行发生错误
        data_len = header['data_len']

        gap_abs = data_len % 1024
        count = data_len // 1024
        recv_data = b''
        for i in range(count):
            data = self.sock.recv(1024)
            print('recv接收的长度是:', len(data))  # 增加此行查看每次循环读取的长度是多少，按理应该是1024
            recv_data += data
        recv_data += self.sock.recv(gap_abs)

        print('recv data len is:', len(recv_data))
        return recv_data

    def send_command(self, cmd):
        self.sock.send(cmd)

    def ask(self, cmd):
        self.sock.send(cmd)
        return self.sock.recv(2048)

    def recv(self):
        return self.sock.recv(2048)

    def set_keepalive(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 2)
