# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/21 9:11
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : common.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/21 : create new
# ----------------------------------------------------------------

import re
import time
import os
import functools
import inspect
import random
import string
import subprocess
import configparser
from datetime import datetime


class IniOperation:
    def __init__(self):
        self.conf = configparser.ConfigParser()

    @property
    def sections(self):
        return self.conf.sections()

    def load_file(self, fp):
        self.conf.read(fp)

    def get_options(self, section):
        return self.conf.options(section)

    def read(self, section, option):
        return self.conf.get(section, option)


def isValidIp(ip):
    if re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$", ip):
        return True
    return False


def isValidMac(mac):
    if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac):
        return True
    return False


def rm_file(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
    return True


def get_current_time_str(fmt="%Y%m%d%H%M%S%f"):
    return datetime.now().strftime(fmt)


def get_random_str(length=5):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def get_secret_key(n: int = 16):
    """
    返回一个有n个byte那么长的一个string，用于加密。
    :param len: 期望返回字符串的byte长度
    :return: 随机生成的字符串
    """
    return os.urandom(n)


def get_current_function_name():
    """
    获取当前执行函数的函数名
    """
    return inspect.stack()[1][3]


def run_cmd(cmd: str):
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = res.communicate()
    return out.decode('gbk')
