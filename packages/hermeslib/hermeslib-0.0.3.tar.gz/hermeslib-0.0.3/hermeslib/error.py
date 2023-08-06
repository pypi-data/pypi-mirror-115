# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 14:51
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : error.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 :
# ----------------------------------------------------------------


class SockConnectionError(Exception):
    """
    socket连接异常
    """

    def __init__(self, host, msg):
        self.host = host
        self.msg = msg

    def __str__(self):
        return (f'[Socket connection error] : Cannot connect to {self.host}, error: {self.msg}')


class UnexpectKeyError(Exception):
    def __init__(self, key: str, exception: list):
        self.key = key
        self.exception = exception

    def __str__(self):
        return (f'[Unexpect key error] : unexcept: {self.key}, exceptted in: {self.exception}')


class UnexpectValueError(Exception):
    def __init__(self, value: str, exception: list):
        self.value = value
        self.exception = exception

    def __str__(self):
        return (f'[Unexpect value error] : got: {self.value}, exceptted in: {self.exception}')


class NotExistError(Exception):
    def __init__(self, target):
        self.target = target

    def __str__(self):
        return (f'The operation target {self.target} is not exist.')


class NotReservedError(Exception):

    def __str__(self):
        return (f'The operation target is not reserved yet,please reserve the operation target first.')


class ProtocolMissingKeyError(Exception):

    def __init__(self, protocol: str, key: str):
        self.protocol = protocol
        self.key = key

    def __str__(self):
        return (f'The protocol ({self.protocol}) missing required key ({self.key}).')
