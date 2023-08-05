# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/19 10:45
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : chassis.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/19 : create new
# ----------------------------------------------------------------

import time
from .base import ApiBase


class ChassisApi(ApiBase):
    APIS = ['connect_chassis', 'disconnect_chassis', 'get_chassis_cfg', 'set_chassis_cfg', 'reserve_chassis',
            'release_chassis', 'reset_chassis']

    def connect_chassis(self, host: str = None, port: int = None, pwd: str = None, owner: str = None) -> tuple:
        """
        连接仪表机框
        :param host: 仪表服务IP
        :param port: 仪表服务端口号
        :param pwd: 仪表连接密码
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 连接成功 0: 连接失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical(host, port, pwd, owner):
            if host is None:
                host = self.config.XENA_SEVER_IP
            if port is None:
                port = self.config.XENA_SEVER_PORT
            if pwd is None:
                pwd = self.config.XENA_DEFAULT_PWD
            if owner is None:
                owner = self.config.DEFAULT_USER

            self.log(f'Instrument connection: host:{host} port:{port} pwd:{pwd} owner:{owner}')

            # 建立与仪表的socket连接
            self.chassis.runner.connect(host, port)
            # 登录仪表
            self.chassis.login(pwd)
            # 设置仪表用户
            self.chassis.owner(owner)
            return ''

        success_msg = 'Connection succeed'
        fail_msg = '[Chassis connection error]'
        param = {'host': host, 'port': port, 'pwd': pwd, 'owner': owner}

        return self._exec_func(logical, param=param, success_msg=success_msg, fail_msg=fail_msg, connect_check=False)

    def disconnect_chassis(self) -> tuple:
        """
        断开仪表连接即退出仪表登录
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 断开连接成功 0: 断开连接失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical():
            # 登出
            self.chassis.logoff()
            # 修改状态
            self.chassis.runner.is_connected = False
            return ''

        success_msg = 'Disconnect successful'
        fail_msg = '[Chassis disconnection error]'

        return self._exec_func(logical, success_msg=success_msg, fail_msg=fail_msg)

    def get_chassis_cfg(self) -> tuple:
        """
        获取仪表配置信息
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 信息获取成功 0: 信息获取失败
                元素2: 数据信息,为字典类型
                元素3: 状态描述
        """

        def logical():
            self.log('Get config data from chassis.')
            cfg = {}
            # 仪表基本信息
            info_resp = self.chassis.info()
            cfg.update(self.runner.format_cfg_resp(info_resp, 'C_'))
            # 仪表配置信息
            cfg_resp = self.chassis.config()
            cfg.update(self.runner.format_cfg_resp(cfg_resp, 'C_'))
            return cfg

        success_msg = 'Data get successfully'
        fail_msg = '[Chassis config get error]'

        return self._exec_func(logical, success_msg=success_msg, fail_msg=fail_msg)

    def set_chassis_cfg(self, **kwargs) -> tuple:
        """
        配置仪表相关参数
        :param kwargs:
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 配置成功 0: 配置失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical():
            for key, value in kwargs.items():
                if key == 'comment':
                    self.chassis.comment(value)
                elif key == 'password':
                    self.chassis.password(value)
                elif key == 'dhcp':
                    self.chassis.dhcp(value)
                elif key == 'hostname':
                    self.chassis.hostname(value)
                elif key == 'ipadress':
                    [address, subnetmask, gateway] = value.split(' ')
                    self.chassis.ipadress(address, subnetmask, gateway)
                elif key == 'flash':
                    self.chassis.flash(value)
                else:
                    raise Exception(f'Unexpected config key: {key}')
                self.log(f'Setting {key} to {value} successful')
            return

        success_msg = 'All chassis config setting succeed'
        fail_msg = '[Chassis config setting error]'

        return self._exec_func(logical, success_msg=success_msg, fail_msg=fail_msg)

    def release_chassis(self) -> tuple:
        """
        释放仪表
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 仪表释放成功 0: 仪表释放失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical():
            self.log('Start releasing the chassis.')
            # 先查询机框状态
            status = self.chassis.reservation()
            # 闲置状态
            if 'RELEASED' in status:
                pass
            # 被自己占用
            elif 'RESERVED_BY_YOU' in status:
                # 直接释放
                self.chassis.reservation('RELEASE')
            # 被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 释放他人连接
                self.chassis.reservation('RELINQUISH')
            return ''

        success_msg = 'Chassis release successful'
        fail_msg = '[Chassis release error]'

        return self._exec_func(logical, success_msg=success_msg, fail_msg=fail_msg)

    def reserve_chassis(self) -> tuple:
        """
        占用仪表
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 仪表占用成功 0: 仪表占用失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical():
            self.log('Start reserving the chassis.')
            # 先查询机框状态
            status = self.chassis.reservation()
            # 闲置状态
            if 'RELEASED' in status:
                # 直接占用
                self.chassis.reservation('RESERVE')
            # 已被自己占用
            elif 'RESERVED_BY_YOU' in status:
                pass
            # 已被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 先释放他人连接
                self.chassis.reservation('RELINQUISH')
                # 再占用
                self.chassis.reservation('RESERVE')
            return ''

        success_msg = 'Chassis reserve successful'
        fail_msg = '[Chassis reserve error]'

        return self._exec_func(logical, success_msg=success_msg, fail_msg=fail_msg)

    def reset_chassis(self) -> tuple:
        """
        重置仪表即重置仪表所有端口
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 所有端口重置成功 0: 所有端口重置失败
                元素2: 数据信息,默认为空
                元素3: 状态描述
        """

        def logical():
            self.log('Start resetting the chassis.')
            # 先占用仪表
            self.reserve_chassis()
            # 查询仪表配置信息
            code, data, msg = self.get_chassis_cfg()
            # 取端口信息
            port_counts = data.get('PORTCOUNTS')
            for index, counts in enumerate(port_counts.split(' ')):
                module = index
                for port_index in range(int(counts)):
                    id = f'{module}/{port_index}'
                    # 重置端口
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
                    # 释放端口
                    self.port.reservation(id, 'RELEASE')
            time.sleep(2)
            return ''

        success_msg = 'Chassis reset successful'
        fail_msg = '[Chassis reset error]'

        return self._exec_func(logical, success_msg=success_msg, fail_msg=fail_msg)
