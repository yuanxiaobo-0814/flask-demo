
from flask import request
from flask_restful import Resource

from app.utils.exceptions import invalid_obj, MissingArgumentError


class BaseHandler(Resource):

    @staticmethod
    def response_format(data, code=200, message='ok'):
        response = {'data': data, 'code': code, 'message': message}
        return response

    @staticmethod
    def get_argument(arg, dft=invalid_obj, required=True, type_=None):
        """从请求中获取参数, 单个"""
        args = dict()
        args.update(request.args.to_dict())
        args.update(request.form.to_dict())
        args.update(request.json or {})
        value = args.get(arg, dft)
        if value is invalid_obj and required:
            raise MissingArgumentError('Argument `{}` is required'.format(arg))
        if type_:
            value = type_(value)
        return value
