#! /usr/bin/env python
# coding: utf-8

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def to_dict(self, include_keys=None, exclude_keys=None):
    """database obj trans to dict, trans column datetime to str
    :param self
    :param include_keys   need keys
    :param exclude_keys   no need keys
    """
    if not self:
        return {}
    data = {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}
    iter_type = (list, tuple, set, dict)
    if include_keys and isinstance(include_keys, iter_type):
        data = {k: v for k, v in data.items() if k in include_keys}
    if exclude_keys and isinstance(exclude_keys, iter_type):
        data = {k: v for k, v in data.items() if k not in exclude_keys}
    for k, v in data.items():
        if isinstance(v, datetime):
            data[k] = v.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(v, date):
            data[k] = v.strftime('%Y-%m-%d')
    return data


db.Model.to_dict = to_dict
