#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Author  : youshu.Ji
import codecs
import os
import json
import pickle
import time
# dir ----------------------------------------------------------------------
def j_mkdir(name):
    if not os.path.exists(name):
        os.mkdir(name)


def get_filename(path):
    '''
    返回路径最后的文件名
    :param path:
    :return:
    '''
    # path = r'哲学-已标记208本-抽取后人工校正版20200316/2哲学-已标记/中国传统价值观诠释学（刘翔）.txt'
    filename = os.path.split(path)[-1]
    return filename


# TODO 还没写
def walk():
    paths = os.walk(r'F:\python_project\tmp_data\njubook_data\标注的图书_标注数据')
    for root, dir, files in paths:
        for name in files:
            if name == 'predict.tf_record':
                os.remove(os.path.join(root, name))


def j_listdir(dir_name, including_dir=True):
    # ATTENTION yield是
    filenames = os.listdir(dir_name)
    for filename in filenames:
        if including_dir:
            yield os.path.join(dir_name, filename)
        else:
            yield filename

# 合并文件 TODO 还没写
def imgrate_files(path):
    filenames = os.listdir(path)
    return None

