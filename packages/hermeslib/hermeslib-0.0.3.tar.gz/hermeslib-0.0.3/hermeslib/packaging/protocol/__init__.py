# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 16:25
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : __init__.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

from .Ethernet import Ethernet
from .IPV4 import Ipv4
from .TCP import Tcp
from .UDP import Udp

PRTOCOL_LAYER = {
    'L2': ['ethernet'],
    'L3': ['ipv4'],
    'L4': ['tcp', 'udp']
}

PROTOCOL_TARGET = {
    'ethernet': Ethernet,
    'ipv4': Ipv4,
    'tcp': Tcp,
    'udp': Udp
}
