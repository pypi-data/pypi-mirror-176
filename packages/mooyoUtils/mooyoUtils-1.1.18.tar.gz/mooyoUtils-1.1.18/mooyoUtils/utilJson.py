#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @time     : 2022/11/16 14:55
# @Author   : new
# @File      : utilJson.py
import ast
from mooyoUtils.logger import logger


def is_immutable(k):
    return isinstance(k, int) or isinstance(k, float) or isinstance(k, tuple)


class HandleJson:
    def __init__(self, data):
        if not data:
            logger.error('请输入json格式数据')
            exit()

        if isinstance(data, str):
            try:
                self.data = ast.literal_eval(data)
            except Exception as e:
                logger.error(f'请输入正确的json格式数据， 报错为:{e}')
                exit()
        elif isinstance(data, dict):
            self.data = data
        else:
            logger.error(f"数据不符合预期， 类型为[{type(data)}]")

    def __paths(self, data, path=''):
        """
        用于遍历json树
        :param data: 原始数据，或者key对应的value值
        :param path: key值字符串，默认值为''
        :return:
        """
        if isinstance(data, dict):
            for k, v in data.items():
                if is_immutable(k):
                    tmp = path + f"[{k}]"
                else:
                    tmp = path + f"['{k}']"

                yield tmp, v
                yield from self.__paths(v, tmp)

        if isinstance(data, list):
            for k, v in enumerate(data):
                tmp = path + f'[{k}]'
                yield tmp, v
                yield from self.__paths(v, tmp)

    def find_key_path(self, key):
        """
        查找key路径
        :param key: 需要查找路径的key值
        :return: 包含key值路径的list
        """
        result = []
        for path, value in self.__paths(self.data):
            if is_immutable(key):
                k = f"[{key}]"
            else:
                k = f"['{key}']"

            if path.endswith(k):
                result.append(path)
        return result

    def find_value_path(self, key):
        """
        查找某个值的路径
        :param key: 需要查找的值，限制为字符串，数字，浮点数，布尔值
        :return:
        """
        result = []
        for path, value in self.__paths(self.data):
            if isinstance(value, (str, int, bool, float)):
                if value == key:
                    result.append(path)
        return result

