#! /usr/bin/env python
# coding: utf-8

from flask import jsonify


invalid_obj = object()


class ErrorJsonResponse(RuntimeError):
    status_code = 400

    def __init__(self, message, status_code=None, data=None):
        if status_code is not None:
            self.status_code = status_code
        self.data = jsonify(dict(code=self.status_code, data=data, message=message))

    def to_dict(self):
        response = self.data
        response.status_code = self.status_code
        return response


class PermissionDenied(ErrorJsonResponse):
    status_code = 403


class ValidationError(ErrorJsonResponse):
    status_code = 424


class MissingArgumentError(ErrorJsonResponse):
    status_code = 424
