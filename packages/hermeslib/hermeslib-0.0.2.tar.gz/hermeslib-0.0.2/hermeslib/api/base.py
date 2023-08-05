# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/21 10:39
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : base.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/21 : create new
# ----------------------------------------------------------------

from ..util.logger import record_api_log
from ..config import config, Config
from ..scripts.runner import Runner
from ..scripts.chassis import Chassis
from ..scripts.module import Module
from ..scripts.port import Port
from ..scripts.stream import Stream


class ApiBase():
    def __init__(self, cfg: Config = None):
        self.config = cfg if cfg != None else config
        self.log = record_api_log
        self.runner = Runner()
        self.runner.set_switch(is_print=self.config.SOCK_IS_PRINT, in_file=self.config.SOCK_IN_FILE)
        self.chassis = Chassis(self.runner)
        self.module = Module(self.runner)
        self.port = Port(self.runner)
        self.stream = Stream(self.runner)

    def _format_result(self, code=1, data=None, msg=None):
        return code, data, msg

    def connect_check(self):
        if not self.runner.is_connected:
            raise Exception('Please establish the connection before performing the operation')

    def _exec_func(self, func, param: dict = None, success_msg='Succeed', fail_msg='Failed', connect_check=True):
        code = 1
        data = None
        msg = success_msg
        try:
            if connect_check:
                self.connect_check()
            data = func(**param) if param else func()
        except Exception as e:
            code = 0
            msg = fail_msg + ':' + str(e)
        self.log(msg)
        return self._format_result(code, data, msg)

    def _exec_func_by_id_or_name(self, func, param, success_msg='Succeed', fail_msg='Failed', id_map: dict = None,
                                 param_deal=None, connect_check=True):
        """
        根据ID列表遍历执行函数
        :param func: 执行函数
        :param id:
        :param name:
        :param id_map:
        :return:
        """
        code = 1
        data = None
        msg = success_msg
        try:
            if connect_check:
                self.connect_check()
            if param_deal:
                if id_map:
                    param = param_deal(param, id_map)
                else:
                    param = param_deal(param)
            data = func(**param) if param else func()
        except Exception as e:
            code = 0
            msg = fail_msg + ':' + str(e)
        self.log(msg)
        return self._format_result(code, data, msg)

    def _deal_id_or_name(self, param: dict, id_map: dict = None):
        id = param.get('id')
        name = param.get('name')
        if id:
            param['name'] = id
        elif name:
            _id = id_map.get(name)
            if not _id:
                raise ValueError(f'Unexpected value: {name}')
            param['id'] = _id
        else:
            raise Exception('Required parameter missing, id or name is required.')
        return param
