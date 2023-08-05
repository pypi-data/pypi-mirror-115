# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/28 10:37
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : test3layer.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/28 : create new
# ----------------------------------------------------------------

def process1():
    from ..api.action import Action
    action = Action()
    # 连接仪表
    resp = action.run(func_name="connect_chassis", host='192.168.1.200', pwd='xena', owner='process1')
    print(resp)
    # 占用仪表（打流非必须）
    resp = action.run(func_name="reserve_chassis")
    print(resp)
    # 占用板卡（打流非必须）
    resp = action.run(func_name="reserve_module", id='6')
    print(resp)
    # 占用端口
    resp = action.run(func_name="reserve_port", name='port1')
    print(resp)
    resp = action.run(func_name="reserve_port", name='port2')
    print(resp)
    # 端口初始化
    resp = action.run(func_name="reset_port", name='port1')
    print(resp)
    resp = action.run(func_name="reset_port", name='port2')
    print(resp)
    # 重置仪表
    resp = action.run(func_name="reserve_chassis")
    print(resp)
    # 释放占用
    resp = action.run(func_name="release_chassis")
    print(resp)
    return


def process2():
    """
    三层流业务测试demo
    :return:
    """

    import time
    from ..api.chassis import ChassisApi
    from ..api.module import ModuleApi
    from ..api.port import PortApi
    from ..api.stream import StreamApi

    # 实例化操作对象
    capi = ChassisApi()  # 机框操作对象
    mapi = ModuleApi()  # 板卡操作对象
    papi = PortApi()  # 端口操作对象
    sapi = StreamApi()  # 流操作对象

    stream_up1 = {
        'name': 'up1',
        'txport': 'port2',
        'rxport': 'port1',
        'rate': 50,
        'rate_unit': 'kbps',
        'frame_size_min': 512,
        'frame_size_max': 512,
        'src_mac': '00:10:94:20:19:02',
        'dst_mac': 'AC:8D:34:31:2A:A7',
        'ipv4_gateway': '192.168.100.1',
        'src_ip': '192.168.100.110',
        'dst_ip': '20.1.1.252',
        'udp_src_port': 3001,
        'udp_dst_port': 3002
    }

    stream_down1 = {
        'name': 'down1',
        'txport': 'port1',
        'rxport': 'port2',
        'rate': 100,
        'rate_unit': 'kbps',
        'frame_size_min': 512,
        'frame_size_max': 512,
        'src_mac': '00:10:94:00:00:A2',
        'dst_mac': 'AC:8D:34:31:2A:A8',
        'svlan_id': 100,
        'src_ip': '20.1.1.252',
        'dst_ip': '20.1.1.1',
        'ipv4_gateway': '20.1.1.1',
        'udp_src_port': 3002,
        'udp_dst_port': 3001
    }
    stream_up2 = {
        'name': 'up2',
        'txport': 'port2',
        'rxport': 'port1',
        'rate': 50,
        'rate_unit': 'kbps',
        'frame_size_min': 512,
        'frame_size_max': 512,
        'src_mac': '00:10:94:20:19:01',
        'dst_mac': 'AC:8D:34:31:2A:A7',
        'ipv4_gateway': '192.168.100.1',
        'src_ip': '192.168.100.109',
        'dst_ip': '20.1.1.251',
        'tcp_src_port': 2001,
        'tcp_dst_port': 2002
    }

    stream_down2 = {
        'name': 'down2',
        'txport': 'port1',
        'rxport': 'port2',
        'rate': 100,
        'rate_unit': 'kbps',
        'frame_size_min': 512,
        'frame_size_max': 512,
        'src_mac': '00:10:94:00:00:A1',
        'dst_mac': 'AC:8D:34:31:2A:A8',
        'svlan_id': 100,
        'src_ip': '20.1.1.251',
        'dst_ip': '20.1.1.1',
        'ipv4_gateway': '20.1.1.1',
        'tcp_src_port': 2002,
        'tcp_dst_port': 2001
    }

    streams = [stream_up1, stream_down1, stream_up2, stream_down2]
    txports = []
    rxports = []

    for stream in streams:
        txport = stream.get('txport')
        if txport not in txports:
            txports.append(txport)
        rxport = stream.get('rxport')
        if rxport not in rxports:
            rxports.append(rxport)

    # 连接仪表
    resp = capi.connect_chassis(pwd='xena', owner='process2')
    print(resp)

    # 占用仪表
    resp = capi.reserve_chassis()
    print(resp)

    for port in set(txports + rxports):
        # 占用端口
        resp = papi.reserve_port(name=port)
        print(resp)
        # 端口初始化
        resp = papi.reset_port(name=port)
        print(resp)

    # # 根据存储的流配置信息创建流
    # resp = sapi.load_stream_config(fp='test.yaml')
    # print(resp)

    for stream in streams:
        # 创建流
        resp = sapi.create_stream(**stream)
        print(resp)

    for port in set(rxports):
        # 清除端口统计信息
        resp = papi.clear_port_statistics(name=port)
        print(resp)

    # time.sleep(6000)

    # 开始打流
    # # 以流为粒度
    # for stream in streams:
    #     resp = sapi.start_stream(name=stream.get('name'),arp_first=1)
    #     print(resp)
    # 以端口为粒度
    for port in txports:
        resp = papi.traffic_start(name=port, arp_first=1)
        print(resp)

    # 开始端口抓包
    for port in rxports:
        resp = papi.capture_start(name=port)
        print(resp)

    # 打流时长
    time.sleep(5)

    # 停止端口抓包
    for port in rxports:
        resp = papi.capture_stop(name=port)
        print(resp)

    # 停止打流
    # # 以流为粒度
    # for stream in streams:
    #     resp = sapi.stop_stream(name=stream.get('name'))
    #     print(resp)
    # 以端口为粒度
    for port in txports:
        resp = papi.traffic_stop(name=port)
        print(resp)

    time.sleep(1)

    # 获取统计信息
    for stream in streams:
        resp = sapi.get_stream_statistics(name=stream.get('name'))
        print(resp)

    # 获取端口抓包数据
    for port in rxports:
        resp = papi.get_capture_data(name=port, is_store=True)
        print(resp)

    # # 获取流配置信息
    # resp = sapi.get_stream_cfg(name=stream_data.get('name'))
    # print(resp)

    # 存储流配置信息至文件
    resp = sapi.save_config_in_file(fp='test.yaml')
    print(resp)

    # 删除流
    for stream in streams:
        resp = sapi.delete_stream(name=stream.get('name'))
        print(resp)

    for port in set(txports + rxports):
        # 端口初始化
        resp = papi.reset_port(name=port)
        print(resp)
        # 释放端口
        resp = papi.release_port(name=port)
        print(resp)

    # 释放机框
    resp = capi.release_chassis()
    print(resp)


if __name__ == '__main__':
    process2()
