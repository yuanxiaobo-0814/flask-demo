#! /usr/bin/env python
# coding: utf-8

import os
import re
import json
import time
from ast import literal_eval
from datetime import datetime, date
from flask import jsonify
from urllib import request

from .exceptions import invalid_obj


def get_env(name, *, default=None, convert=False):
    """get environment variable from file .env"""
    try:
        env_value = os.getenv(name)
        return literal_eval(env_value) if convert else env_value
    except:
        return default


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def recover_short_url(url):
    fake_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:13.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2500.0 Safari/537.36',
    }
    try:
        req = request.Request(url, headers=fake_headers)
        res = request.urlopen(req)
        r_url = res.geturl()
        return r_url
    except Exception as e:
        print("url:{0}, err:{1}".format(url, e))
        return url


def strftime(datetime_obj, format='%Y-%m-%d %H:%M:%S'):
    if not datetime_obj:
        return
    return datetime_obj.strftime(format)


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def response_format(data, code, message):
    response = {'data': data, 'code': code, 'message': message}
    return jsonify(response)


def split_string_and_convert_into_int(text):
    """拆分字符串并转化为整数型

    Args:
        text: 字符串

    Returns:
        set 类型
    """
    if not text:
        return set()
    return set(map(int, text.split(',')))


def get_variable_from_sql(sql):
    variable = re.findall(r'\'\${\s*(\w+)\s*}\'', sql)
    return variable


def replace_cluster_query_variable(sql, variable, value):
    pattern = r'\'\${\s*%s\s*}\'' % variable
    if not isinstance(value, str):
        value = str(value)
    sql = re.sub(pattern, value, sql)
    return sql


def trim(string):
    # string = string.decode("unicode-escape")
    if string.startswith("'"):
        string = string[1:]
    if string.startswith("u'"):
        string = string[2:]
    if string.endswith("'"):
        string = string[:len(string) - 1]
    if string.endswith("', ';"):
        string = string[:len(string) - 5]
    return string


class ObjectDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def to_int(s, dft=0, e_raise=False):
    """trans obj to int, if failed, if e_raise, raise, if not e_raise, return dft"""
    try:
        s = int(float(str(s)))
        return s
    except ValueError:
        if e_raise:
            raise ValueError('`{}` cannot trans to int'.format(s))
        else:
            return dft


def iter_filter(iter_, dft=invalid_obj, func=None, e_raise=True):
    data_type = type(iter_)
    data = []
    if func and callable(func):
        for d in iter_:
            try:
                data.append(func(d))
            except:
                if dft is not invalid_obj:
                    data.append(dft)
                else:
                    if e_raise:
                        raise ValueError('`{} can not trans to {}`'.format(d, func.__name__))
    return data_type(data)
