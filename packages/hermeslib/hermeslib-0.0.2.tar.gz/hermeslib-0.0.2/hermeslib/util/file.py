# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/16 15:14
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : file.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/16 : create new
# ----------------------------------------------------------------

import re
import yaml
from ..config import config
from ..util import run_cmd


def write_yaml(data, fp: str):
    with open(fp, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
    return


def read_yaml(fp: str):
    with open(fp, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def cut_text(text, lenth):
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr


def hex2pcap(hex_datas: list, temp_path='temp.txt', store_fp='formatted.pcap'):
    lines = []
    for hex_data in hex_datas:
        hex_data = hex_data[2:]
        hex_data_lines = cut_text(hex_data, 32)
        for index, line_data in enumerate(hex_data_lines):
            line_dl = cut_text(line_data, 2)
            offset = str(hex(int(index * 16))).lstrip('0x').zfill(4)
            line_dl.insert(0, offset)
            line_str = ' '.join(line_dl) + '\n'
            lines.append(line_str)
    with open(temp_path, encoding='utf-8', mode='w+') as f:
        f.writelines(lines)

    cmd = f'{config.TEXT2PCAP_PATH} {temp_path} {store_fp}'
    data = run_cmd(cmd)
    return True
