# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/19 10:46
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : port.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/19 : create new
# ----------------------------------------------------------------

import os
import time
from .base import ApiBase
from ..error import NotReservedError
from ..util.common import isValidMac, isValidIp, get_current_time_str
from ..util.file import hex2pcap


class PortApi(ApiBase):
    APIS = ['release_port', 'reserve_port', 'reset_port', 'get_port_cfg', 'set_port_cfg', 'traffic_start',
            'traffic_stop', 'enable_port', 'disable_port', 'get_port_rate', 'set_port_rate', 'set_port_mac',
            'set_port_ip', 'enable_ping', 'disable_ping', 'enable_arp', 'disable_arp', 'capture_start',
            'capture_stop', 'set_capture_condition', 'get_capture_data', 'clear_port_statistics',
            'clear_transmit_statistics', 'clear_receive_statistics']

    def release_port(self, id: str = None, name: str = None):
        """
        释放端口
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口释放成功 0: 端口释放失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start releasing the port [{name}].')
            # 先查询端口状态
            status = self.port.reservation(id)
            # 闲置状态
            if 'RELEASED' in status:
                pass
            # 被自己占用
            elif 'RESERVED_BY_YOU' in status:
                # 直接释放
                self.port.reservation(id, 'RELEASE')
            # 被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 释放他人连接
                self.port.reservation(id, 'RELINQUISH')
            self.log(f'Port [{name}] released.')
            return ''

        success_msg = 'Port release successful'
        fail_msg = '[Port release error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def reserve_port(self, id: str = None, name: str = None):
        """
        占用端口
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口释放成功 0: 端口释放失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start reserving the port [{name}].')
            # 先查询端口状态
            status = self.port.reservation(id)
            # 闲置状态
            if 'RELEASED' in status:
                # 直接占用
                self.port.reservation(id, 'RESERVE')
            # 已被自己占用
            elif 'RESERVED_BY_YOU' in status:
                pass
            # 已被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 先释放他人连接
                self.port.reservation(id, 'RELINQUISH')
                # 再占用
                self.port.reservation(id, 'RESERVE')
            self.log(f'Port [{name}] reserved.')
            return ''

        success_msg = 'Port reserve successful'
        fail_msg = '[Port reserve error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def reset_port(self, id: str = None, name: str = None):
        """
        占用端口
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口重置成功 0: 端口重置失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start resetting the port [{name}].')
            # 先查询端口状态
            status = self.port.reservation(id)
            # 闲置状态
            if 'RELEASED' in status:
                # 直接占用
                self.port.reservation(id, 'RESERVE')
            # 已被自己占用
            elif 'RESERVED_BY_YOU' in status:
                pass
            # 已被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 先释放他人连接
                self.port.reservation(id, 'RELINQUISH')
                # 再占用
                self.port.reservation(id, 'RESERVE')
            # 占用后执行重置
            self.port.reset(id)
            time.sleep(5)

            self.log(f'Port [{name}] reset.')
            return ''

        success_msg = 'Port reset successful'
        fail_msg = '[Port reset error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def get_port_cfg(self, ids: list = None, names: list = None) -> tuple:
        """
        获取端口配置信息
        :param ids: 存储端口ID的列表
        :param names: 存储端口名称的列表
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口配置信息获取成功 0: 端口配置信息获取失败
                元素2: 存储获取的端口配置信息的字典
                元素3: 状态描述
        """

        def get_one_cfg(id):
            cfg = {}
            # 端口基本信息
            info_resp = self.port.info(id)
            if info_resp != '<BADMODULE>':
                cfg.update(self.runner.format_cfg_resp(info_resp, 'P_', 1))
                # 端口配置信息
                cfg_resp = self.port.config(id)
                cfg.update(self.runner.format_cfg_resp(cfg_resp, 'P_', 1))
            else:
                pass
            return cfg

        code = 1
        msg = 'Data get successful'
        all_cfg = {}
        self.log('Get config data from port.')
        try:
            if ids:
                for id in ids:
                    all_cfg[id] = get_one_cfg(id)
            elif names:
                for name in names:
                    id = name
                    all_cfg[name] = get_one_cfg(id)
            else:
                raise Exception('Required parameter missing')
        except Exception as e:
            code = 0
            msg = '[Port config get error] :' + str(e)

        self.log(msg)
        return self._format_result(code, data=all_cfg, msg=msg)

    def set_port_cfg(self, id: str = None, name: str = None, **kwargs):
        """
        修改端口配置信息
        :param id:
        :param name:
        :param kwargs:
        :return:
        """
        for key, value in kwargs.items():
            pass
        return 1

    def traffic_start(self, id: str = None, name: str = None, arp_first: int = 0):
        """
        端口启动打流
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口启动打流成功 0: 端口启动打流失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None, arp_first=0):
            self.log(f'Start port [{name}] traffic.')
            # 先查询端口配置信息
            code, data, desc = self.get_port_cfg(ids=[id])
            if code == 1:
                port_cfg = data.get(id)
                if port_cfg.get('RESERVATION') != 'RESERVED_BY_YOU':
                    raise NotReservedError()
                if port_cfg.get('TRAFFIC') == 'ON':
                    raise Exception('The port traffic is already started.')
                # 查询是否有流配置信息
                dlen, data = self.runner.format_one_line_resp(self.stream.indices(id))
                if dlen == 2:
                    raise Exception(
                        f'There is no stream exist under the port [{name}],please create stream first.')
                if dlen == 3:
                    self.port.arpreplay(id, 'ON')
                    time.sleep(1)
                    sids = data[2].split(' ')
                    for sid in sids:
                        # 打流前先发arp
                        if arp_first:
                            try:
                                self.stream.arp_request(id, sid)
                            except Exception as e:
                                print(e)
                        # 设置流状态
                        self.stream.enable(id, sid, 'ON')
                # 端口启动打流
                self.port.traffic(id, 'ON')
            else:
                raise Exception(desc)
            self.log(f'Port [{name}] traffic started.')
            return ''

        success_msg = 'Port traffic start successfully'
        fail_msg = '[Port traffic start error]'
        param = {'id': id, 'name': name, 'arp_first': arp_first}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def traffic_stop(self, id: str = None, name: str = None):
        """
        端口停止打流
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口停止打流成功 0: 端口停止打流失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Stop port [{name}] traffic.')
            # 先查询端口配置信息
            code, data, desc = self.get_port_cfg(ids=[id])
            if code == 1:
                port_cfg = data.get(id)
                if port_cfg.get('RESERVATION') != 'RESERVED_BY_YOU':
                    raise NotReservedError()
                if port_cfg.get('TRAFFIC') != 'ON':
                    raise Exception('The port traffic is not in running status.')
                # 端口停止打流
                self.port.traffic(id, 'OFF')
                # 查询流配置信息
                dlen, data = self.runner.format_one_line_resp(self.stream.indices(id))
                if dlen == 3:
                    sids = data[2].split(' ')
                    for sid in sids:
                        # 设置流状态
                        self.stream.enable(id, sid, 'SUPPRESS')
            else:
                raise Exception(desc)
            self.log(f'Port [{name}] traffic stopped.')
            return ''

        success_msg = 'Port traffic stop successfully'
        fail_msg = '[Port traffic stop error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def enable_port_tx(self, id: str = None, name: str = None):
        """
        端口使能传输
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口使能成功 0: 端口使能失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start enable port [{name}] .')
            self.port.enable_tx(id, 'ON')
            self.log(f'Port [{name}] enabled.')
            return ''

        success_msg = 'Port enable successfully'
        fail_msg = '[Port enable error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def disable_port_tx(self, id: str = None, name: str = None):
        """
        去使能端口传输
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口去使能成功 0: 端口去使能失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start disable port [{name}] .')
            self.port.enable_tx(id, 'OFF')
            self.log(f'Port [{name}] disabled.')
            return ''

        success_msg = 'Port disable successfully'
        fail_msg = '[Port disable error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def get_port_rate(self, id: str = None, name: str = None):
        """
        查询端口速率
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口速率查询成功 0: 端口速率查询失败
                元素2: 端口速率信息
                元素3: 状态描述
        """

        def logical(id, name=None):
            rate = ''
            unit = ''
            self.log(f'Start query port [{name}] rate.')
            dlen, data = self.runner.format_one_line_resp(self.port.rate(id))
            if dlen != 3:
                raise Exception('')
            rate = data[2]
            if 'PPS' in data[1]:
                unit = 'pps'
            elif 'BPS' in data[1]:
                unit = 'bps'
            self.log(f'Port [{name}] rate {rate} {unit}.')
            return {'rate': rate, 'unit': unit}

        success_msg = 'Port rate query succeed'
        fail_msg = '[Port rate query error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def set_port_rate(self, id: str = None, name: str = None, rate: int = None, unit: str = 'bps'):
        """
        设置端口速率
        :param id: 端口ID
        :param name: 端口名称
        :param rate: 速率值
        :param unit: 速率单位 pps,bps,kpps,kbps,mpps,mbps
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口速率设置成功 0: 端口速率设置失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name, rate, unit):
            self.log(f'Start disable port [{name}] .')
            # 根据单位换算速率值
            if 'm' == unit.lower()[0]:
                rate = rate * 1000000
            elif 'k' == unit.lower()[0]:
                rate = rate * 1000
            if 'bps' in unit.lower():
                # 速率单位 bps
                self.port.ratel2bps(id, rate)
            elif 'pps' in unit.lower():
                # 速率单位 pps
                self.port.ratepps(id, rate)
            else:
                self.port.ratefraction(id, rate)
            self.log(f'Port [{name}] disabled.')
            return ''

        success_msg = 'Port rate setting successful'
        fail_msg = '[Port rate setting error]'
        param = {'id': id, 'name': name, 'rate': rate, 'unit': unit}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def set_port_mac(self, id: str = None, name: str = None, mac: str = None):
        """
        设置端口Mac地址
        :param id: 端口ID
        :param name: 端口名称
        :param name: mac地址字符串如: AA:BB:CC:DD:EE:FF
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口Mac地址设置成功 0: 端口Mac地址设置失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name, mac):
            self.log(f'Start set port [{name}] mac.')
            if not isValidMac(mac):
                raise Exception(f'The mac address [{mac}] is not valid.')
            mac = '0x' + mac.replace(':', '')
            self.port.macadress(id, mac)
            self.log(f'Port [{name}] mac {mac}.')
            return ''

        success_msg = 'Port mac setting successful'
        fail_msg = '[Port mac setting error]'
        param = {'id': id, 'name': name, 'mac': mac}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def set_port_ip(self, id: str = None, name: str = None, address: str = None, subnet: str = None,
                    gateway: str = None, wild: str = None):
        """
        设置端口IP地址
        :param id: 端口ID
        :param name: 端口名称
        :param address:
        :param subnet:
        :param gateway:
        :param wild:
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口IP地址设置成功 0: 端口IP地址设置失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name, address, subnet, gateway, wild):
            self.log(f'Start set port [{name}] ip.')
            for ip in [address, subnet, gateway, wild]:
                if not isValidIp(address):
                    raise Exception(f'The IP [{ip}] is not valid.')
            self.port.ipaddress(id, address, subnet, gateway, wild)
            self.log(f'Port [{name}] IP {address}.')
            return ''

        success_msg = 'Port IP setting successful'
        fail_msg = '[Port IP setting error]'
        param = {'id': id, 'name': name, 'address': address, 'subnet': subnet, 'gateway': gateway, 'wild': wild}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def enable_ping(self, id: str = None, name: str = None):
        """
        启用端口ping功能
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口ping功能启用成功 0: 端口ping功能启用失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Enable port [{name}] ping.')
            self.port.pingreplay(id, 'ON')
            self.log(f'Port [{name}] ping enabled.')
            return ''

        success_msg = 'Port ping enable successfully'
        fail_msg = '[Port ping enable error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def disable_ping(self, id: str = None, name: str = None):
        """
        停用端口ping功能
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口ping功能停用成功 0: 端口ping功能停用失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Disable port [{name}] ping.')
            self.port.pingreplay(id, 'OFF')
            self.log(f'Port [{name}] ping disabled.')
            return ''

        success_msg = 'Port ping disable successfully'
        fail_msg = '[Port ping disable error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def enable_arp(self, id: str = None, name: str = None):
        """
        启用端口arp功能
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口arp功能启用成功 0: 端口arp功能启用失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Enable port [{name}] arp.')
            self.port.arpreplay(id, 'ON')
            self.log(f'Port [{name}] arp enabled.')
            return ''

        success_msg = 'Port arp enable successfully'
        fail_msg = '[Port arp enable error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def disable_arp(self, id: str = None, name: str = None):
        """
        停用端口ping功能
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口ping功能停用成功 0: 端口ping功能停用失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Disable port [{name}] arp.')
            self.port.arpreplay(id, 'OFF')
            self.log(f'Port [{name}] arp disabled.')
            return ''

        success_msg = 'Port arp disable successfully'
        fail_msg = '[Port arp disable error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def capture_start(self, id: str = None, name: str = None):
        """
        端口启动抓包
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口启动抓包成功 0: 端口启动抓包失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start port [{name}] capture.')
            # 先查询端口配置信息
            code, data, desc = self.get_port_cfg(ids=[id])
            if code == 1:
                port_cfg = data.get(id)
                if port_cfg.get('RESERVATION') != 'RESERVED_BY_YOU':
                    raise NotReservedError()
                if port_cfg.get('CAPTURE') == 'ON':
                    raise Exception('The port capture is already started.')
                self.port.capture(id, 'ON')
            else:
                raise Exception(desc)
            self.log(f'Port [{name}] capture started.')
            return ''

        success_msg = 'Port capture start successfully'
        fail_msg = '[Port capture start error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def capture_stop(self, id: str = None, name: str = None):
        """
        端口停止抓包
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口停止抓包成功 0: 端口停止抓包失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Stop port [{name}] capture.')
            # 先查询端口配置信息
            code, data, desc = self.get_port_cfg(ids=[id])
            if code == 1:
                port_cfg = data.get(id)
                if port_cfg.get('RESERVATION') != 'RESERVED_BY_YOU':
                    raise NotReservedError()
                if port_cfg.get('CAPTURE') != 'ON':
                    raise Exception('The port capture is not in running status.')
                self.port.capture(id, 'OFF')
            else:
                raise Exception(desc)
            self.log(f'Port [{name}] capture stopped.')
            return ''

        success_msg = 'Port capture stop successfully'
        fail_msg = '[Port capture stop error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def set_capture_condition(self, id: str = None, name: str = None):
        """
        设置端口抓包条件
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口停止抓包成功 0: 端口停止抓包失败
                元素2: 抓包数据
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Stop port [{name}] capture.')
            # 先查询端口配置信息
            code, data, desc = self.get_port_cfg(ids=[id])
            if code == 1:
                port_cfg = data.get(id)
                if port_cfg.get('RESERVATION') != 'RESERVED_BY_YOU':
                    raise NotReservedError()
                if port_cfg.get('CAPTURE') != 'ON':
                    raise Exception('The port capture is not in running status.')
                self.port.capture(id, 'OFF')
            else:
                raise Exception(desc)
            self.log(f'Port [{name}] capture stopped.')
            return ''

        success_msg = 'Port capture stop successfully'
        fail_msg = '[Port capture stop error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def get_capture_data(self, id: str = None, name: str = None, is_store: bool = False, fp: str = None):
        """
        获取端口抓包数据
        :param id: 端口ID
        :param name: 端口名称
        :param is_store: 是否存储抓包数据
        :param fp: 抓包数据存储文件路径
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 获取端口抓包数据成功 0: 获取端口抓包数据失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name, fp):
            self.log(f'Start getting port [{name}] capture data.')
            cap_data = []
            dlen, data = self.runner.format_one_line_resp(self.port.stats(id))
            if dlen != 3:
                raise Exception()
            packets = data[2].split(' ')[1]
            for cid in range(int(packets)):
                dlen, one_data = self.runner.format_one_line_resp(self.port.packet(id, cid))
                if dlen == 4:
                    cap_data.append(one_data[3])
                else:
                    print(one_data)
            self.log(f'Port [{name}] capture data got over,package count: {len(cap_data)}.')
            if is_store:
                if fp != None:
                    if os.path.splitext(fp)[-1].lower() != '.pcap':
                        raise Exception(f'Unexpected file type:{os.path.splitext(fp)[-1]}')
                    if not os.path.dirname(fp):
                        fp = os.path.join(self.config.STREAM_CAP_STORE_PATH, fp)
                else:
                    fp = os.path.join(self.config.STREAM_CAP_STORE_PATH, get_current_time_str() + '.pcap')
                temp_path = os.path.join(self.config.STREAM_CAP_STORE_PATH, 'temp.txt')
                hex2pcap(cap_data, temp_path, fp)
                self.log(f'Capture data record in: {fp}.')
                return fp
            else:
                return cap_data

        success_msg = 'Get port capture data successfully'
        fail_msg = '[Get port capture data error]'
        param = {'id': id, 'name': name, 'fp': fp}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def clear_transmit_statistics(self, id: str = None, name: str = None):
        """
        清除端口发包数据统计
        Clear all the transmit statistics for a port. The byte and packet counts will restart at zero.
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口发包统计数据清理成功 0: 端口发包统计数据清理失败
                元素2: 空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start clearing port [{name}] transmit statistics.')
            self.port.pt_clear(id)
            self.log(f'Port [{name}] transmit statistics cleared.')
            return ''

        success_msg = 'Clear port transmit statistics successfully'
        fail_msg = '[Clear port transmit statistics error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def clear_receive_statistics(self, id: str = None, name: str = None):
        """
        清除端口收包数据统计
        Clear all the receive statistics for a port. The byte and packet counts will restart at zero.
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口收包统计数据清理成功 0: 端口收包统计数据清理失败
                元素2: 空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start clearing port [{name}] receive statistics.')
            self.port.pr_clear(id)
            self.log(f'Port [{name}] receive statistics cleared.')
            return ''

        success_msg = 'Clear port receive statistics successfully'
        fail_msg = '[Clear port receive statistics error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)

    def clear_port_statistics(self, id: str = None, name: str = None):
        """
        清除端口数据统计
        :param id: 端口ID
        :param name: 端口名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 端口统计数据清理成功 0: 端口统计数据清理失败
                元素2: 空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start clearing port [{name}] statistics data.')
            self.port.pr_clear(id)
            self.port.pt_clear(id)
            self.log(f'Port [{name}] statistics data cleared.')
            return ''

        success_msg = 'Clear port statistics data successfully'
        fail_msg = '[Clear port statistics data error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.PORT_MAPPING)
