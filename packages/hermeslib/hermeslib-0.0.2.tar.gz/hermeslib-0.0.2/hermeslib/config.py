# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 15:15
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : config.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

import os
from .util.common import IniOperation


class Config(object):
    XENA_SEVER_IP = '192.168.1.200'  # 测试仪IP
    XENA_SEVER_PORT = 22611  # 测试仪服务端口
    XENA_DEFAULT_PWD = 'xena'  # 仪表连接密码
    DEFAULT_USER = 'hermes'  # 仪表操作默认用户名
    ROOT_PATH = r'C:\valkyrie'  # 仪表操作存储文件默认根目录
    TEXT2PCAP_PATH = ''  # 将text转换为pcap文件的可执行程序的绝对路径
    LOG_MODE = 'print'  # 日志输出形式 print:控制台输出 file:记录于日志文件
    SOCK_IS_PRINT = False
    SOCK_IN_FILE = False
    API_IS_PRINT = False
    API_IN_FILE = False
    MODULE_MAPPING = {}  # 模块映射字典
    PORT_MAPPING = {}  # 端口映射字典

    def __init__(self, fp: str = None):
        # 读取配置文件，更新默认配置
        if fp == None:
            fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        io = IniOperation()
        io.load_file(fp)
        sections = io.sections
        server_host = io.read('instrument_cfg', 'host')
        if server_host:
            self.XENA_SEVER_IP = server_host
        server_port = int(io.read('instrument_cfg', 'port'))
        if server_port:
            self.XENA_SEVER_PORT = server_port
        default_pwd = io.read('instrument_cfg', 'default_pwd')
        if default_pwd:
            self.XENA_DEFAULT_PWD = default_pwd
        default_user = io.read('instrument_cfg', 'default_user')
        if default_user:
            self.DEFAULT_USER = default_user
        store_root = io.read('file_path', 'store_root')
        if store_root:
            self.ROOT_PATH = store_root
        self.STREAM_CFG_STORE_PATH = os.path.join(self.ROOT_PATH, 'stream_cfg')
        self.STREAM_CAP_STORE_PATH = os.path.join(self.ROOT_PATH, 'stream_cap')
        text2pcap_path = io.read('file_path', 'text2pcap_path')
        if text2pcap_path:
            self.TEXT2PCAP_PATH = text2pcap_path
        log_mode = io.read('log', 'log_mode')
        if log_mode:
            self.LOG_MODE = log_mode
        socket_is_print = int(io.read('log', 'socket_is_print'))
        if socket_is_print:
            self.SOCK_IS_PRINT = socket_is_print
        socket_in_file = int(io.read('log', 'socket_in_file'))
        if socket_in_file:
            self.SOCK_IN_FILE = socket_in_file
        api_is_print = int(io.read('log', 'api_is_print'))
        if api_is_print:
            self.API_IS_PRINT = api_is_print
        api_in_file = int(io.read('log', 'api_in_file'))
        if api_in_file:
            self.API_IN_FILE = api_in_file
        modules = io.get_options('module_mapping')
        for module in modules:
            self.MODULE_MAPPING[module] = io.read('module_mapping', module)
        ports = io.get_options('port_mapping')
        for port in ports:
            self.PORT_MAPPING[port] = io.read('port_mapping', port)


config = Config()
