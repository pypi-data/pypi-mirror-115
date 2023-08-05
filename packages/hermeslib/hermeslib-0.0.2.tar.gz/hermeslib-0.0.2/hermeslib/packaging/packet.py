# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 16:26
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : packet.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

from .protocol import PROTOCOL_TARGET, PRTOCOL_LAYER


class Packet:

    def __init__(self):
        self.remain_len = self.package_len = 128
        self.length = 0
        self.protocols = {}

    def add_protocol(self, layer=None, protocol=None, **kwargs):
        """
        设置数据包各层相应协议的属性值
        :param layer: 协议所属层级，可选值L2,L3,L4
        :param protocol: 协议类型关键字，如ethernet,ipv4
        :param kwargs: 设置协议属性值对应的传参
        :return:
        """
        if not layer or layer not in PRTOCOL_LAYER.keys():
            raise Exception('缺少协议层级参数或参数非法')
        if protocol and protocol in PRTOCOL_LAYER.get(layer):
            layer_info = self.protocols.get(layer)
            if not layer_info:
                layer_info = {
                    'protocol': protocol,
                    'param': {}
                }
            _portocol = layer_info.get('protocol')
            if _portocol and _portocol != protocol:
                raise Exception('')
            _property = layer_info.get('param')
            _property.update(kwargs)
            self.protocols[layer] = layer_info
        else:
            raise Exception('缺少协议类型参数或参数非法')
        return

    def header_property(self, layer: str = None):
        """
        取数据包各层相应协议的属性值
        :param layer: 协议所属层级，可选值L2,L3,L4
        :param protocol: 协议类型关键字，如ethernet,ipv4
        :param kwargs: 设置协议属性值对应的传参
        :return:
        """
        dict = {}

        for key, value in self.protocols:
            target = self.__getattribute__(value)
            dict.update(target.property)
        return dict

    def set_packet_property(self, **kwargs):
        """
        设置数据包属性值
        属性：
            protocols:数据包所包含的所有协议
            length：数据包包长
        :param kwargs: 属性参数
        :return:
        """
        for key, value in kwargs.items():
            if key == 'length':
                self.package_len = self.remain_len = value
            self.__setattr__(key, value)

    def get_packet_property(self, key):
        """
        获取数据包属性值
        :param key: 属性关键字
        :return: 获取的属性值
        """
        return self.__getattribute__(key)

    @property
    def packet_header(self):
        """
        根据各层协议组装数据包协议头
        """
        # 数据包报头所包含的协议
        contain_protocol = []
        # 报头字符串
        header = ''
        layers = sorted(self.protocols.keys())
        for index, layer in enumerate(layers):
            # 协议类型
            protocol = self.protocols[layer].get('protocol')
            # 协议对象初始化需要的参数
            param = self.protocols[layer].get('param')
            # 得到初始化的协议对象
            target = PROTOCOL_TARGET.get(protocol)()
            if 'next_protocol' in target.PROPERTY:
                if 'next_protocol' not in param.keys():
                    if index + 1 != len(self.protocols.keys()):
                        next_protocol = self.protocols[layers[index + 1]].get('protocol')
                    else:
                        next_protocol = '0'
                    param['next_protocol'] = next_protocol
            # 设置协议参数
            target.set_property(**param)
            # 传入协议所包含的数据长度
            target.remain_len = int(self.remain_len)
            # 获取对应协议的数据头
            header += target.protocol_header
            # 计算剩余长度
            self.remain_len -= target.real_len
            contain_protocol.extend(target.get_hname)

        return contain_protocol, '0x' + header.upper()

    def parse_header(self, protocol, header, **kwargs):
        target = PROTOCOL_TARGET.get(protocol)()
        return target.format_min_header(header, kwargs)
