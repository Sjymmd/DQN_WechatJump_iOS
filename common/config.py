# -*- coding: utf-8 -*-
"""
调取配置文件和屏幕分辨率的代码
"""
import os
import sys
import json
import re
from PIL import Image

def open_accordant_config():

    screen_size = _get_screen_size()
    config_file = "{}/config/iPhone/{screen_size}".format(sys.path[0],screen_size=screen_size)
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("Load config file from {}".format(config_file))
            return json.load(f)
    else:
        with open('{}/config/default.json'.format(sys.path[0]), 'r') as f:
            print("Load default config")
            return json.load(f)


def _get_screen_size():

    im = Image.open("Iphone.png")
    if im.size[0]<800:
        return "8_config.json"
    else:
        return "X_config.json"

if __name__=='__main__':
    open_accordant_config()