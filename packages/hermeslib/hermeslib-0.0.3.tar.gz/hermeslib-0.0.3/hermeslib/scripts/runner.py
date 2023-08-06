# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/19 8:57
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : runner.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/19 : create new
# ----------------------------------------------------------------

import sys
import time
import threading
from ..util.sock import SocketDriver
from ..util.logger import record_log
from ..error import NotExistError, NotReservedError


class Runner:
    def __init__(self):
        self.access_semaphor = threading.Semaphore(1)
        self.is_connected = False
        self.is_print = False
        self.in_file = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(Runner, "_instance"):
            Runner._instance = object.__new__(cls)
        return Runner._instance

    def connect(self, hostname, port=22611):
        self._record_log(f"connect to host: {hostname} port: {port}")
        self.driver = SocketDriver(hostname, port)
        self.driver.set_keepalive()
        self.is_connected = True

    def set_switch(self, **kwargs):
        switch_list = ['is_print', 'in_file']
        for key, value in kwargs.items():
            if key in switch_list:
                self.__setattr__(key, value)
        return self

    def _record_log(self, log_str, level='info'):
        return record_log(log_str, self.is_print, self.in_file, level)

    def _error_exist(self, error_msg='Error Exist !'):
        self._record_log(error_msg, 'error')
        # sys.exit(1)

    def _cmd_processed(self, cmd):
        """
        all lines sent to the chassis must be terminated by CR/LF.
        :param cmd:
        :return:
        """
        return cmd.encode() + b'\n'

    def ask(self, cmd,wait=0):
        def exec(cmd):
            resp = b''
            null_count = 0
            one_before = b''
            while True:
                res = self.driver.ask(self._cmd_processed(cmd))
                cmd = ''
                t_res = res.strip(b'\n').strip(b' ')
                if t_res:
                    null_count = 0
                    if one_before != t_res:
                        resp += res
                        one_before = t_res
                else:
                    if null_count > 2:
                        break
                    else:
                        null_count += 1
                # print(null_count,res.decode().strip('\n'))
            if isinstance(resp, bytes):
                resp = resp.decode()
            return resp.strip('\n')

        self._record_log(f"Ask cmd     : {cmd}")
        self.access_semaphor.acquire()
        resp = exec(cmd)
        if not resp and wait:
            time.sleep(wait)
            resp = self.driver.recv()
            if isinstance(resp, bytes):
                resp = resp.decode().strip('\n')
        self.access_semaphor.release()
        if 'PC_PACKET' not in resp:
            #
            self._record_log(f"Ask received: {resp}")
        if 'Syntax error' in resp:
            raise Exception(f'Syntax error,please check the cmd parameter and try again. cmd: {cmd} ,error desc:{resp}')
        elif '<NOTRESERVED>' == resp:
            # 返回 <NOTRESERVED> 说明当前操作需要先预留操作对象
            raise NotReservedError()
        elif '<NOTVALID>' == resp:
            # 返回 <NOTVALID> 说明当前操作无效
            raise Exception('The operation is not valid.')
        elif '<BADMODULE>' == resp:
            module = cmd.split(' ')[0].strip()
            raise NotExistError(f'module [{module}]')
        elif '<BADPORT>' == resp:
            port = cmd.split(' ')[0].strip()
            raise NotExistError(f'port [{port}]')

        return resp

    def ask_wait(self, cmd, wait=0):
        resp = self.ask(cmd)
        if not resp:
            time.sleep(wait)
            resp = self.driver.recv()
        return resp

    def send_expect(self, cmd, expect):
        resp = self.ask(cmd)
        if resp == expect:
            return True
        else:
            raise Exception(f"Unexpected value. Expected: {expect}, Received: {resp}")

    def send_expect_ok(self, cmd):
        return self.send_expect(cmd, '<OK>')

    def format_cfg_resp(self, resp: str, prefix='C_', sub: int = 0):
        formatted = {}
        # 去除首尾换行符
        resp = resp.strip('\n')
        # 拆分出一行行数据
        resp_lines = resp.split('\n')
        # 去除首尾换行符
        for line in resp_lines:
            line_info = line.split('  ')
            line_info = line_info[sub:]
            if len(line_info) == 2:
                formatted[line_info[0].replace(prefix, '')] = line_info[1].strip('"')
            else:
                print(line_info)
        return formatted

    def format_one_line_resp(self, line_str: str):
        data = [x.strip() for x in line_str.split('  ') if x.strip()]
        return len(data), data
