# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 14:51
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : __init__.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 :
# ----------------------------------------------------------------

import subprocess


def run_cmd(cmd: str):
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = res.communicate()
    return out.decode('gbk')

