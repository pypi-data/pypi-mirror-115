# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 17:14
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : stream.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

from .packet import Packet


class Stream():
    COMMON_PROPERTY = ['name', 'txport', 'rxport', 'rate', 'rate_unit', 'frame_size_min', 'frame_size_max',
                       'frame_size_type', 'payload_hex', 'payload_type']

    def __init__(self, name):
        self.packet = Packet()
        # 流名称
        self.name = name
        # 流状态
        self.is_running = False
        # 流ID(预留)
        self.sid = None
        # Test Payload ID (TID),Test payload identifier used to identify the sending stream.
        self.tid = None
        # 发包端口
        self.txport = None
        # 收包端口
        self.rxport = None
        # 打流速率
        self.rate = None
        # 打流速率单位
        self.rate_unit = None

        # 打流数据帧帧长最小值（单位：字节）
        self.frame_size_min = None
        # 打流数据帧帧长最大值（单位：字节）
        self.frame_size_max = None
        # 打流数据帧帧长类型
        self.frame_size_type = 'FIXED'

        self.payload_hex = '0x00'
        self.payload_type = 'PATTERN'

        # 流数据包包含的网络协议
        self.contain_protocols = []
        # 数据包报头字符串
        self.packet_header = ''

    def set_layer_property(self, layer: str, protocol: str, params: dict):
        self.packet.add_protocol(layer, protocol, **params)

    def setL2(self, params: dict, protocol: str = 'ethernet'):
        """
        设置流二层协议内容
        :param params: 协议参数
        :param protocol: 协议类型如 ethernet
        :return:
        """
        self.packet.add_protocol('L2', protocol, **params)

    def setL3(self, params: dict, protocol: str = 'ipv4'):
        """
        设置流三层协议内容
        :param params: 协议参数
        :param protocol: 协议类型如 ipv4
        :return:
        """
        self.packet.add_protocol('L3', protocol, **params)

    def setL4(self, params: dict, protocol: str = 'udp'):
        """
        设置流四层协议内容
        :param params: 协议参数
        :param protocol: 协议类型如 tcp、udp
        :return:
        """
        self.packet.add_protocol('L4', protocol, **params)

    def direction(self, txport, rxport):
        self.txport = txport
        self.rxport = rxport

    def bandwidth(self, load=10, load_unit='mbps'):
        """
        设置发流带宽
        :param load: 发流速率数值
        :param load_unit: 发流速率单位
        :return:
        """
        self.rate = int(load)
        self.rate_unit = load_unit

    def framesize(self, min: int = 512, max: int = 512, type: str = 'FIXED'):
        """
        设置报文长度
        :param frame_size: 长度值，单位为字节
        :return:
        """
        self.frame_size_min = min
        self.frame_size_max = max
        self.frame_size_type = type

    def payload(self, hex: str, type: str = 'PATTERN'):
        self.payload_hex = hex
        self.payload_type = type

    def streamid(self, sid, tid):
        self.sid = sid
        self.tid = tid

    @property
    def stream_create_cfg(self):
        """
        获取仪表创建流所需要的参数
        :return:
        """
        self.packet.set_packet_property(length=self.frame_size_min)
        self.contain_protocols, self.packet_header = self.packet.packet_header
        cfg = {}
        needs = ['name', 'rate', 'rate_unit', 'frame_size_min', 'frame_size_max', 'frame_size_type',
                 'contain_protocols', 'packet_header', 'payload_hex', 'payload_type']
        for key in needs:
            value = self.__getattribute__(key)
            if value:
                cfg[key] = value
            else:
                raise Exception(f'Missing required value for a stream config,keyword: {key}')
        return cfg

    def header_property(self, layer: str = None):
        """
        获取流协议头属性值
        :param layer: 协议所属层级，可选值L2,L3,L4,如果不传默认取所有层级
        :return:
        """
        dict = {}
        if layer:
            layer_info = self.packet.protocols.get(layer)
            if layer_info:
                dict.update(layer_info.get('param'))
        else:
            for layer, layer_info in self.packet.protocols.items():
                if layer_info:
                    dict.update(layer_info.get('param'))
        dict.pop('next_protocol')
        return dict

    @property
    def stream_cfg(self):
        """
        获取流配置信息
        :return: 配置信息
        """
        cfg = {}
        # 获取配置信息
        for key in self.COMMON_PROPERTY:
            cfg[key] = self.__getattribute__(key)
        cfg.update(self.header_property())
        return cfg

    def parse_header(self, protocols: list, header: str):
        parsed_data = {}
        protocol = ''
        return self.packet.parse_header(protocol=protocol, header=header)
