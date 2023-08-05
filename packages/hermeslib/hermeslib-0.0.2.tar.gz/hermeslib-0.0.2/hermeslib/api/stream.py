# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/19 10:46
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : stream.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/19 : create new
# ----------------------------------------------------------------

import os
import time
from .base import ApiBase
from ..packaging.stream import Stream
from ..util.common import get_current_time_str
from ..util.file import read_yaml, write_yaml

LAYER_PROTOCOL_PROPERTY = {
    'L2': {
        'ethernet': ['src_mac', 'dst_mac', 'cvlan_id', 'svlan_id', 'cvlan_pri']
    },
    'L3': {
        'ipv4': ['src_ip', 'dst_ip', 'ipv4_gateway', 'ip_pri', 'service_type', 'dscp'],
        'ipv6': ['src_ipv6', 'dst_ipv6', 'ipv6_gateway']
    },
    'L4': {
        'udp': ['udp_src_port', 'udp_dst_port'],
        'tcp': ['tcp_src_port', 'tcp_dst_port'],
        'igmp': ['igmp_type', 'group_address'],
        'icmp': ['icmp_type', 'icmp_code']
    }
}


class StreamControl(ApiBase):
    def __init__(self):
        super().__init__()
        self.sids = []
        self.tids = []
        self.all_streams = dict()

    @property
    def _new_id(self):
        sid = self.sids[-1] + 1 if self.sids else 0
        tid = self.tids[-1] + 1 if self.tids else 0
        return sid, tid

    def id_by_name(self, name):
        """
        根据流名称返回流对象
        :param name: 流名称
        :return:
        """
        stream = self.all_streams.get(name)
        if not stream:
            raise Exception(f'Stream [{name}] not exist.')
        # 实际操作的端口值
        port = self.config.PORT_MAPPING.get(stream.txport)
        sid = stream.sid
        tid = stream.tid
        return port, sid, tid, stream

    def set_stream_property(self, stream: Stream, **kwargs):
        """
        设置流属性
        :param stream: 流对象
        :param kwargs: 属性参数
        :return:
        """
        for key, value in kwargs.items():
            has_set = False
            # 设置共有属性
            if key in stream.COMMON_PROPERTY:
                stream.__setattr__(key, value)
                has_set = True
            else:
                # 设置特有报头
                for layer, protocols in LAYER_PROTOCOL_PROPERTY.items():
                    for protocol, properties in protocols.items():
                        for property in properties:
                            if property == key:
                                param = {key: value}
                                stream.set_layer_property(layer, protocol, param)
                                has_set = True
            if not has_set:
                raise Exception(f'Unexpected key: {key}')

    def create(self, **kwargs):
        """
        创建流
        :param kwargs: 流创建参数
        :return:
        """
        stream_name = kwargs.get('name')
        if not stream_name:
            raise Exception(f'Missing required param.')
        # 校验是否已存在同一名称的流
        if self.all_streams.get(stream_name):
            raise Exception(f'The stream name of {stream_name} is already exist.')
        stream = Stream(stream_name)
        self.set_stream_property(stream, **kwargs)
        return stream

    def status_check_before_update(self, stream: Stream):
        """
        执行流属性更新操作之前校验流是否处于运行状态，运行中不允许修改
        :param stream: 流对象
        :return:
        """
        if stream.is_running:
            raise Exception(
                'Cannot change stream property when the stream is in running status,please stop the stream first.')

    def _format_stream_cfg(self, resp: str):
        formatted = {}
        # 去除首尾换行符
        resp = resp.strip('\n')
        # 拆分出一行行数据
        resp_lines = resp.split('\n')
        # 去除首尾换行符
        for line in resp_lines:
            line_info = line.split('  ')
            if len(line_info) == 4:
                [port, cmd, sid, param] = line_info
                cmd = cmd.replace('PS_', '')
                sid = sid.strip('[]')
                if not formatted.get(sid):
                    formatted[sid] = {}
                formatted[sid][cmd] = param
            else:
                print(line_info)
        return formatted

    def _parse_stream_cfg(self, cfg: dict):
        parsed_data = {}
        for key, value in cfg.items():
            if key == 'COMMENT':
                parsed_data['name'] = value
            elif key == 'RATEL2BPS':
                value = int(value)
                rate_unit = 'bps'
                if value > 1000 and value < 1000000:
                    value = value / 1000
                    rate_unit = 'kbps'
                if value > 1000000:
                    value = value / 1000000
                    rate_unit = 'mbps'
                parsed_data['rate'] = value
                parsed_data['rate_unit'] = rate_unit
            elif key == 'PACKETLENGTH':
                value = value.split(' ')
                parsed_data['frame_size_type'] = value[0]
                parsed_data['frame_size_min'] = value[1]
                parsed_data['frame_size_max'] = value[2]
            elif key == 'HEADERPROTOCOL' and value:
                protocols = value.split(' ')
                header = cfg.get('')
                parsed_data.update(self.get_parsed_header(protocols, header))

        return parsed_data

    def get_parsed_header(self, protocols: list, header: str):
        select_data = {}
        stream = Stream('temp')
        header_data = stream.parse_header(protocols, header)
        for layer, protocols in LAYER_PROTOCOL_PROPERTY.items():
            for protocol, properties in protocols.items():
                if protocol in header_data.keys():
                    for property in properties:
                        value = header_data.get(protocol).get(property)
                        if value != None:
                            select_data[property] = value
        return select_data


class StreamApi(ApiBase):
    APIS = ['create_stream', 'delete_stream', 'update_stream_status', 'start_stream', 'stop_stream',
            'update_stream_length', 'update_stream_rate', 'get_stream_cfg', 'send_arp', 'send_ping',
            'update_stream_payload', 'get_stream_statistics', 'update_stream_cfg', 'save_config_in_file',
            'load_stream_config']

    def __init__(self):
        super().__init__()
        self.control = StreamControl()

    def create_stream(self, name: str = None, txport: str = None, rxport: str = None,
                      rate: int = None, rate_unit: str = None,
                      frame_size_min: int = None, frame_size_max: int = None, frame_size_type: str = None,
                      payload_hex: str = None, payload_type: str = None,
                      src_mac: str = None, dst_mac: str = None,
                      svlan_id: int = None, cvlan_id: int = None, cvlan_pri: int = None,
                      src_ip: str = None, dst_ip: str = None, ipv4_gateway: str = None,
                      service_type: int = None, dscp: int = None,
                      tcp_src_port: str = None, tcp_dst_port: str = None,
                      udp_src_port: str = None, udp_dst_port: str = None):
        """
        创建一条流
        :param name: 流名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1:流创建成功 0: 流创建失败
                元素2: 空
                元素3: 状态描述
        """
        kwargs = locals()
        kwargs.pop('self')

        def logical(**kwargs):
            self.log(f'Start creating stream [{name}] .')
            pkg_stream = self.control.create(**kwargs)
            sid, tid = self.control._new_id
            pkg_stream.sid = sid
            pkg_stream.tid = tid
            port = self.config.PORT_MAPPING.get(pkg_stream.txport)
            stream_cfg = pkg_stream.stream_create_cfg
            # Create the SID index of stream
            self.stream.create(port, sid)
            # Configure the description of stream
            self.stream.comment(port, sid, stream_cfg.get('name'))
            # Configure the stream status
            self.stream.enable(port, sid, 'SUPPRESS')
            # Configure the ipv4_gateway
            ipv4_gateway = param.get('ipv4_gateway')
            if ipv4_gateway:
                self.stream.set_ipv4gateway(port, sid, ipv4_gateway)
            # Create the TPLD index of stream
            self.stream.set_tpldid(port, sid, tid)
            # Configure the stream rate
            rate = stream_cfg.get('rate')
            rate_unit = stream_cfg.get('rate_unit')
            if 'm' == rate_unit.lower()[0]:
                rate = rate * 1000000
            elif 'k' == rate_unit.lower()[0]:
                rate = rate * 1000
            if 'bps' in rate_unit.lower():
                self.stream.set_ratel2bps(port, sid, rate)
            elif 'pps' in rate_unit.lower():
                self.stream.set_ratepps(port, sid, rate)
            else:
                self.stream.set_rate_fraction(port, sid, rate)
            # Configure the packet type
            protocols = stream_cfg.get('contain_protocols')
            self.stream.set_header_protocol(port, sid, *protocols)
            # Configure the packet header
            packet_header = stream_cfg.get('packet_header')
            self.stream.set_packet_header(port, sid, packet_header)
            # Configure the packet size
            self.stream.set_packet_length(port, sid, stream_cfg.get('frame_size_min'),
                                          stream_cfg.get('frame_size_max'),
                                          stream_cfg.get('frame_size_type'))
            # self.ss.update_packetlimit(port, sid, -1)
            self.stream.set_payload(port, sid, '0x00', 'PATTERN')
            self.control.sids.append(sid)
            self.control.tids.append(tid)
            self.control.all_streams[name] = pkg_stream
            self.log(f'Stream [{name}] created.')
            return ''

        success_msg = 'Stream create successfully'
        fail_msg = '[Stream create error]'
        param = {}
        for key, value in kwargs.items():
            if value != None:
                param[key] = value
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def delete_stream(self, name: str = None):
        """
        根据流名称删除流
        :param name: 流名称
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 删除成功 0: 删除失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name=None):
            self.log(f'Start deleting stream [{name}] .')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 检查流状态
            self.control.status_check_before_update(stream)
            # 删除仪表流配置
            self.stream.delete(port, sid)
            # 删除缓存对象流对应信息
            self.control.all_streams.pop(name)
            self.control.sids.remove(sid)
            self.control.tids.remove(tid)
            self.log(f'Stream [{name}] deleted.')
            return ''

        success_msg = 'Stream delete successfully'
        fail_msg = '[Stream delete  error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def update_stream_status(self, name: str = None, status: str = None):
        """
        修改流状态
        :param name: 流名称
        :param status: 状态值   ● OFF (0) (stream will not be used when port traffic is started)
                                ● ON (1) (stream will be started when port traffic is started)
                                ● SUPPRESS (2) (stream will not be started when port traffic is started but can be
                                 started afterwards)
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 流状态更新成功 0: 流状态更新失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name, status):
            self.log(f'Start setting stream [{name}] status.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 设置流状态
            self.stream.enable(port, sid, status)
            # 修改缓存流对象运行状态
            stream.is_running = True if status == 'ON' else False
            self.log(f'Stream [{name}] status set.')
            return ''

        success_msg = 'Stream status setting successfully'
        fail_msg = '[Stream status setting  error]'
        param = {'name': name, 'status': status}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def start_stream(self, name: str = None, arp_first=0):
        """
        根据流名称启动打流
        :param name: 流名称
        :param arp_first: 启动打流前是否先发送arp请求，默认不发送 1发送，0不发送
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 流启动成功 0: 流启动失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name=None):
            self.log(f'Start running stream [{name}] .')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 打流前先发arp
            if arp_first:
                self.port.arpreplay(port, 'ON')
                time.sleep(1)
                self.stream.arp_request(port, sid)
            # 设置流状态
            self.stream.enable(port, sid, 'ON')
            # 设置端口打流状态
            self.port.traffic(port, 'ON')

            # 修改缓存流对象运行状态
            stream.is_running = True

            self.log(f'Stream [{name}] is running.')
            return ''

        success_msg = 'Stream start successfully'
        fail_msg = '[Stream start error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def stop_stream(self, name: str = None):
        """
        停止打流
        :param name: 流名称
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 流停止成功 0: 流停止失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name=None):
            self.log(f'Start stopping stream [{name}] .')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 设置流状态
            self.stream.enable(port, sid, 'SUPPRESS')
            # 修改缓存流对象运行状态
            stream.is_running = False
            self.log(f'Stream [{name}] stopped.')
            return ''

        success_msg = 'Stream stop successfully'
        fail_msg = '[Stream stop error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def update_stream_length(self, name: str = None, min: int = None, max: int = None, type: str = 'FIXED'):
        """
        修改打流数据包长
        :param name: 流名称
        :param min: lower limit on the packet length.
        :param max: upper limit on the packet length.
        :param type:  the kind of distribution:
                    ● FIXED (all packets have min size)
                    ● INCREMENTING (incrementing from min to max)
                    ● BUTTERFLY (min, max, min+1, max-1, min+2, max-2, etc)
                    ● RANDOM (random between min and max)
                    ● MIX (a mixture of sizes between 56 and 1518, average 464 bytes)
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 修改成功 0: 修改失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name, min, max, type):
            self.log(f'Start setting stream [{name}] length.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 检查流状态
            self.control.status_check_before_update(stream)
            # 更新仪表包长
            self.stream.set_packet_length(port, sid, min, max, type)
            # 更新缓存对象数据
            stream.framesize(min, max, type)
            # 更新报头
            self.stream.set_packet_header(port, sid, stream.stream_create_cfg.get('packet_header'))

            self.log(f'Stream [{name}] length set.')
            return ''

        success_msg = 'Stream length setting successful.'
        fail_msg = '[Stream length setting error]'
        param = {'name': name, 'min': min, 'max': max, 'type': type}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def update_stream_rate(self, name: str = None, rate: int = None, rate_unit: str = 'bps'):
        """
        修改打流速率
        :param name: 流名称
        :param rate: 流速率值
        :param rate_unit: 流速单位
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 修改成功 0: 修改失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name, rate, rate_unit):
            self.log(f'Start setting stream [{name}] rate.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 检查流状态
            self.control.status_check_before_update(stream)
            # 单位换算
            if 'm' == rate_unit.lower()[0]:
                rate = rate * 1000000
            elif 'k' == rate_unit.lower()[0]:
                rate = rate * 1000
            if 'bps' in rate_unit.lower():
                self.stream.set_ratel2bps(port, sid, rate)
            elif 'pps' in rate_unit.lower():
                self.stream.set_ratepps(port, sid, rate)
            else:
                self.stream.set_rate_fraction(port, sid, rate)
            # 更新缓存对象数据
            stream.bandwidth(rate, rate_unit)

            self.log(f'Stream [{name}] rate set.')
            return ''

        success_msg = 'Stream rate setting successful.'
        fail_msg = '[Stream rate setting error]'
        param = {'name': name, 'rate': rate, 'rate_unit': rate_unit}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def get_stream_cfg(self, name: str = None):
        """
        根据流名称获取单条流配置信息
        :param name:
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 查询成功成功 0: 查询失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name=None):
            self.log(f'Start getting stream [{name}] config.')
            cfg = {}
            port, sid, tid, stream = self.control.id_by_name(name)
            # 仪表配置信息
            cfg_resp = self.stream.config(port, sid)
            cfg.update(self.control._format_stream_cfg(cfg_resp))
            self.log(f'Stream [{name}] config got.')
            return cfg

        success_msg = 'Stream config get successfully'
        fail_msg = '[Stream config get error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def send_arp(self, name: str = None):
        """
        发送arp请求
        :param name: 流名称
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: arp发送成功 0: arp发送失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name):
            self.log(f'Start sending stream [{name}] arp request.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 发送arp请求
            self.stream.arp_request(port, sid)
            self.log(f'Stream [{name}] arp request sent.')
            return ''

        success_msg = 'Arp request send successfully'
        fail_msg = '[Arp request send error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def send_ping(self, name: str = None):
        """
        发送ping请求
        :param name:
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: ping发送成功 0: ping发送失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name):
            self.log(f'Start sending stream [{name}] ping request.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 发送ping请求
            self.stream.ping_request(port, sid)
            self.log(f'Stream [{name}] ping request sent.')
            return ''

        success_msg = 'Ping request send successfully'
        fail_msg = '[Ping request send error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def update_stream_payload(self, name: str = None, type: str = None, hexdata: str = None):
        """
        修改流的payload
        :param name: 流名称
        :param type: payload类型
                    ● PATTERN (a pattern is repeated up through the packet)
                    ● INCREMENTING (bytes are incremented up through the packet)
                    ● PRBS (bytes are randomized from packet to packet)
                    ● RANDOM (a random generated pattern)
        :param hexdata: 16进制字符串，pattern of bytes to be repeated. The maximum length of the pattern is
                        18 bytes. Only used if type is set to PATTERN.
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 修改成功 0: 修改失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name, type, hexdata):
            self.log(f'Start setting stream [{name}] payload.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 检查流状态
            self.control.status_check_before_update(stream)
            self.stream.set_payload(port, sid, hexdata, type)
            # 更新缓存对象数据
            stream.bandwidth(hexdata, type)
            self.log(f'Stream [{name}] payload set.')
            return ''

        success_msg = 'Stream payload setting successful.'
        fail_msg = '[Stream payload setting error]'
        param = {'name': name, 'type': type, 'hexdata': hexdata}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def get_stream_statistics(self, name: str = None):
        """
        获取打流统计信息
        :param name: 流名称
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 查询成功 0: 查询失败
                元素2: 统计信息
                元素3: 状态描述
        """

        def format_result_resp(resp: str):
            return resp.split('  ')[-1].split(' ')

        def logical(name=None):
            self.log(f'Start getting stream [{name}] statistics.')
            tport, sid, tid, stream = self.control.id_by_name(name)
            stream = self.control.all_streams.get(name)
            rport = self.config.PORT_MAPPING.get(stream.rxport)

            # Get the TX and RX result
            tx = format_result_resp(self.stream.get_stream(tport, sid))[3]  # 发送端口发包数
            rx = format_result_resp(self.stream.get_tpldtraffic(rport, tid))[3]  # 接收端口收包数
            # Get the error
            error = format_result_resp(self.stream.get_tplderrors(rport, tid))
            # Get the FCS
            fcs = format_result_resp(self.stream.get_extra(rport))[0]
            # Caculate the lost
            lost = int(tx) - int(rx)

            self.log(f'stream: {name} → transmit: {tx} ,receive: {rx} ,lost: {lost} .')
            self.log(f'Stream [{name}] statistics got.')
            return {'tx': tx, 'rx': rx, 'misoder_error': error[2], 'payload_error': error[3], 'fcs': fcs, 'lost': lost}

        success_msg = 'Stream statistics get successfully'
        fail_msg = '[Stream statistics get error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def update_stream_cfg(self, name: str = None, **kwargs):
        """
        更新打流参数
        :param name: 流名称
        :param src_mac:
        :param dst_mac:
        :param svlan_id:
        :param cvlan_id:
        :param cvlan_pri:
        :param src_ip:
        :param dst_ip:
        :param ipv4_gateway:
        :param src_port:
        :param dst_port:
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 更新成功 0: 更新失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name=None):
            self.log(f'Start updating stream [{name}] header config data.')
            port, sid, tid, stream = self.control.id_by_name(name)
            # 检查流状态
            self.control.status_check_before_update(stream)
            # 更新缓存流对象属性
            self.control.set_stream_property(stream, **kwargs)
            # 更新仪表流配置
            self.stream.set_packet_header(port, sid, stream.stream_create_cfg.get('packet_header'))
            self.log(f'Stream [{name}] header config updated.')
            return ''

        success_msg = 'Stream header config update successfully'
        fail_msg = '[Stream header config update error]'
        param = {'name': name}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def save_config_in_file(self, name: str = None, fp: str = None):
        """
        存储流配置信息至文件
        :param name: 流名称，为空则存储所有流配置，不为空则存储指定流
        :param fp: 配置文件名
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 配置存储成功 0: 配置存储失败
                元素2: 配置文件存储路径
                元素3: 状态描述
        """

        def logical(name, fp):
            self.log(f'Start saving stream config.')
            cfg_list = []
            if name != None:
                port, sid, tid, stream = self.control.id_by_name(name)
                streams = [stream]
            else:
                streams = self.control.all_streams.values()
            for stream in streams:
                cfg_list.append(stream.stream_cfg)
            # 写入文件
            if fp != None:
                if os.path.splitext(fp)[-1].lower() != '.yaml':
                    raise Exception(f'Unexpected file type:{os.path.splitext(fp)[-1]}')
                if not os.path.dirname(fp):
                    fp = os.path.join(self.config.STREAM_CFG_STORE_PATH, fp)
            else:
                fp = os.path.join(self.config.STREAM_CFG_STORE_PATH, get_current_time_str() + '.yaml')
            write_yaml(cfg_list, fp)
            return fp

        success_msg = 'Stream config save successfully'
        fail_msg = '[Stream config save error]'
        param = {'name': name, 'fp': fp}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)

    def load_stream_config(self, name: str = None, fp: str = None):
        """
        根据存储的流配置信息创建流
        :param name: 流名称，为空则创建所有流配置，不为空则创建指定流
        :param fp: 配置文件名
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 配置读取成功 0: 配置读取失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(name, fp):
            self.log(f'Start loading stream config.')
            # 读文件
            if fp != None:
                if os.path.splitext(fp)[-1].lower() != '.yaml':
                    raise Exception(f'Unexpected file type:{os.path.splitext(fp)[-1]}')
                if not os.path.dirname(fp):
                    fp = os.path.join(self.config.STREAM_CFG_STORE_PATH, fp)
            else:
                raise Exception(f'Missing required param: fp')
            cfg_list = read_yaml(fp)
            if name != None:
                streams = []
                for stream in cfg_list:
                    if stream.get('name') == name:
                        streams.append(stream)
                        break
            else:
                streams = cfg_list
            for stream in streams:
                self.create_stream(**stream)

            return fp

        success_msg = 'Stream config load successfully'
        fail_msg = '[Stream config load error]'
        param = {'name': name, 'fp': fp}
        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg)
