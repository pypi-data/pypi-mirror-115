# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/19 10:46
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : module.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/19 : create new
# ----------------------------------------------------------------

from .base import ApiBase


class ModuleApi(ApiBase):
    APIS = ['get_module_cfg', 'set_module_cfg', 'release_module', 'reserve_module']

    def get_module_cfg(self, mid: list = None, mname: list = None) -> tuple:
        """
        根据板卡名称或板卡ID获取相应的板卡信息，两个参数只取其一如果两个参数同时存在优先取ID的值
        :param mid: 存储板卡ID的列表
        :param mname: 存储板卡名称的列表
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 信息获取成功 0: 信息获取失败
                元素2: 存储板卡信息的字典
                元素3: 状态描述
        """

        def get_one_cfg(id):
            cfg = {}
            # 板卡基本信息
            info_resp = self.module.info(id)
            if info_resp != '<BADMODULE>':
                cfg.update(self.runner.format_cfg_resp(info_resp, 'M_', 1))
                # 板卡配置信息
                cfg_resp = self.module.config(id)
                cfg.update(self.runner.format_cfg_resp(cfg_resp, 'M_', 1))
            else:
                pass
            return cfg

        code = 1
        msg = 'Data get successful'
        all_cfg = {}
        self.log('Get config data from module.')
        try:
            if mid:
                for id in mid:
                    all_cfg[id] = get_one_cfg(id)
            elif mname:
                for name in mname:
                    id = name
                    all_cfg[name] = get_one_cfg(id)
            else:
                raise Exception('Required parameter missing')
        except Exception as e:
            code = 0
            msg = '[Module config get error] :' + str(e)

        self.log(msg)
        return self._format_result(code, data=all_cfg, msg=msg)

    def set_module_cfg(self, id, **kwargs):
        for key, value in kwargs.items():
            pass
        return 1

    def release_module(self, id: str = None, name: str = None):
        """
        根据板卡名称或板卡ID释放板卡，两个参数只取其一如果两个参数同时存在优先取ID的值
        :param id: 板卡ID
        :param name: 板卡名称
        :return: 返回元祖类型数据，共3个元素：
                元素1: 状态码,1: 板卡释放成功 0: 板卡释放失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start releasing the module [{name}].')
            # 先查询板卡状态
            status = self.module.reservation(id)
            # 闲置状态
            if 'RELEASED' in status:
                pass
            # 被自己占用
            elif 'RESERVED_BY_YOU' in status:
                # 直接释放
                self.module.reservation(id, 'RELEASE')
            # 被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 释放他人连接
                self.module.reservation(id, 'RELINQUISH')
            self.log(f'Module [{name}] released.')
            return ''

        success_msg = 'Module release successful'
        fail_msg = '[Module release error]'

        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.MODULE_MAPPING)

    def reserve_module(self, id: str = None, name: str = None):
        """
        根据板卡名称或板卡ID占用板卡，两个参数只取其一如果两个参数同时存在优先取ID的值
        :param id: 板卡ID
        :param name: 板卡名称
        :return: 返回元祖类型数据，共3个元素:
                元素1: 状态码,1: 板卡占用成功 0: 板卡占用失败
                元素2: 数据信息，为空
                元素3: 状态描述
        """

        def logical(id, name=None):
            self.log(f'Start reserving the module [{name}].')
            # 先查询板卡状态
            status = self.module.reservation(id)
            print(status)
            # 闲置状态
            if 'RELEASED' in status:
                # 直接占用
                self.module.reservation(id, 'RESERVE')
            # 已被自己占用
            elif 'RESERVED_BY_YOU' in status:
                pass
            # 已被其他人占用
            elif 'RESERVED_BY_OTHER' in status:
                # 先释放他人连接
                self.module.reservation(id, 'RELINQUISH')
                # 再占用
                self.module.reservation(id, 'RESERVE')
            self.log(f'Module [{name}] reserved.')
            return

        success_msg = 'Module reserve successful'
        fail_msg = '[Module reserve error]'
        param = {'id': id, 'name': name}
        return self._exec_func_by_id_or_name(logical, param=param, success_msg=success_msg, fail_msg=fail_msg,
                                             param_deal=self._deal_id_or_name, id_map=self.config.MODULE_MAPPING)
