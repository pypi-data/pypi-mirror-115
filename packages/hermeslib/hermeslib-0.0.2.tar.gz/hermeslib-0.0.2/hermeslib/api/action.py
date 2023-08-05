# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 16:33
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : action.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

from .base import ApiBase
from .chassis import ChassisApi
from .module import ModuleApi
from .port import PortApi
from .stream import StreamApi


class Action(object):
    def __init__(self):
        self.api_base = ApiBase()
        self.chassis_api = ChassisApi()
        self.module_api = ModuleApi()
        self.port_api = PortApi()
        self.stream_api = StreamApi()

    def run(self, func_name, **func_params):

        if func_name == 'connect_chassis':
            return self.chassis_api.__getattribute__(func_name)(**func_params)
        else:
            if not self.api_base.runner.is_connected:
                raise Exception('Please establish the connection before performing the operation')
            if func_name in self.chassis_api.APIS:
                return self.chassis_api.__getattribute__(func_name)(**func_params)
            elif func_name in self.module_api.APIS:
                return self.module_api.__getattribute__(func_name)(**func_params)
            elif func_name in self.port_api.APIS:
                return self.port_api.__getattribute__(func_name)(**func_params)
            elif func_name in self.stream_api.APIS:
                return self.stream_api.__getattribute__(func_name)(**func_params)
