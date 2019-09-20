#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify


def response_format(data, code, message):
    response = {'data': data, 'code': code, 'message': message}
    return jsonify(response)
