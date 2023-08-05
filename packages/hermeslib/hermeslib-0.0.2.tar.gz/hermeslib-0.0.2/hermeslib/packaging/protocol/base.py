# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 17:33
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : base.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

import socket
from binascii import hexlify
from ...error import ProtocolMissingKeyError


class ProtocolBase:
    PROPERTY = []
    IGNORE_KEY = []

    def __init__(self):
        self.remain_len = 0
        self.min_len = 0
        self.real_len = 0
        self.name = None
        self.protocol_property = []

    def hname(self):
        return [self.name]

    @property
    def get_hname(self):
        return self.hname()

    def remove_char(self, str: str, char=':'):
        """
        :param str:
        :param char:
        :return:
        """
        return str.replace(char, '')

    def get_hex_ip(self, ip):
        """
        进IP地址转化为16进制字符串
        :param ip: IP地址
        :return:
        """
        return hexlify(socket.inet_aton(ip)).decode()

    def int2bin(self, int_str: int, zfill_len: int = None):
        """
        将2进制字符串转化为16进制字符串，返回指定长度字符，不足高位补零
        :param int_str: 十进制数值
        :param zfill_len: 返回字符长度，默认无指定(返回转换后的原值)
        :return:
        """
        value = str(bin(int(int_str))).replace('0b', '')
        if zfill_len != None:
            value = value.zfill(zfill_len)
        return value

    def int2hex(self, int_str: int, zfill_len: int = None):
        """
        将2进制字符串转化为16进制字符串，返回指定长度字符，不足高位补零
        :param int_str: 十进制数值
        :param zfill_len: 返回字符长度，默认无指定(返回转换后的原值)
        :return:
        """
        value = str(hex(int_str)).replace('0x', '')
        if zfill_len != None:
            value = value.zfill(zfill_len)
        return value

    def bin2hex(self, bin_str: str, zfill_len: int = None):
        """
        将2进制字符串转化为16进制字符串，返回指定长度字符，不足高位补零
        :param bin_str: 二进制字符串
        :param zfill_len: 返回字符长度，默认无指定(返回转换后的原值)
        :return:
        """
        value = str(hex(int(bin_str, 2))).replace('0x', '')
        if zfill_len != None:
            value = value.zfill(zfill_len)
        return value

    def hex2bin(self, hex_str: str, zfill_len: int = None):
        """
        将16进制字符串转化为2进制字符串，返回指定长度字符，不足高位补零
        :param hex_str: 16进制字符串
        :param zfill_len: 返回字符长度，默认无指定(返回转换后的原值)
        :return:
        """
        value = str(bin(int(hex_str, 16))).replace('0b', '')
        if zfill_len != None:
            value = value.zfill(zfill_len)
        return value

    def add_str(self, *args):
        _str = ''
        for arg in args:
            _str += str(arg)
        return _str

    def format_min_header(self, header: str, **kwargs):
        if len(header) < self.min_len * 2:
            raise Exception(f'The data length should not be less than {self.min_len * 2},[{self.name}]: {header}')
        return self._exec_format(header, **kwargs)

    @property
    def protocol_header(self):
        """
        返回协议头字符串
        :return:
        """
        header = self._get_header()
        self.real_len = len(header) / 2
        return header

    @property
    def property(self):
        property_dict = {}
        for key in self.PROPERTY:
            value = self.__getattribute__(key)
            if value != None:
                property_dict[key] = value
            else:
                if key not in self.IGNORE_KEY:
                    raise ProtocolMissingKeyError(self.name, key)
        return property_dict

    def set_property(self, **kwargs):
        pass

    def _exec_format(self, header, **kwargs):
        return self.property

    def _get_header(self):
        hex_header = ''
        return hex_header
