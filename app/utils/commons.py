#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import datetime
import decimal

import re

import sqlparse as sqlparse
import xlsxwriter as xlsxwriter
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import DML, Keyword

import utils
from utils.helpers import strftime


def extract_columns(input_sql):
    # 提取查询的字段名
    def extract_name(item):
        new_item = re.sub('\( | \)', '', item)
        return new_item.split(" ")[-1].strip()

    sql = input_sql.replace("\n", " ").replace("`", "")
    tokens = sqlparse.parse(sql)[0].tokens
    columns = []
    for token in tokens:
        if isinstance(token, Identifier):
            return [extract_name(token.value)]
        if not token.is_group:
            if token.value == 'date':
                columns.append(token.value)
            elif token.value == 'from':
                return columns
        elif isinstance(token, IdentifierList):
            for item in token:
                if item.value == ",":
                    continue
                cname = extract_name(item.value)
                if len(cname) > 0:
                    if "." in cname:
                        tmp_name = cname.split(".")[-1]
                        res = re.sub('\(|\)', '', tmp_name)
                        columns.append(res)
                    else:
                        columns.append(cname)
    return columns


def extract_columns_with_auth(input_sql, unauth=[]):
    # 提取查询的字段名
    def extract_name(item):
        new_item = re.sub('\( | \)', '', item)
        return new_item.split(" ")[-1].strip()

    if not unauth or len(unauth) == 0:
        return input_sql
    input_sql = input_sql.replace("\n", " ").replace("`", "")
    tokens = sqlparse.parse(input_sql)[0].tokens
    columns, origin_columns = [], []
    for token in tokens:
        if isinstance(token, Identifier):
            return [extract_name(token.value)]
        if not token.is_group:
            if token.value == 'date':
                columns.append('date')
                origin_columns.append('date')
            elif token.value == 'from':
                return ' '.join(['select', ','.join(origin_columns), input_sql[input_sql.find('from') - 1:]])
        elif isinstance(token, IdentifierList):
            for item in token:
                if item.value == ",":
                    continue
                origin_cname = item.value
                cname = extract_name(item.value)
                if len(cname) > 0:
                    origin_columns.append(origin_cname)
                    if "." in cname:
                        tmp_name = cname.split(".")[-1]
                        res = re.sub('\(|\)', '', tmp_name)
                        columns.append(res)
                    else:
                        columns.append(cname)
            del_indexs = []
            for i, c in enumerate(columns):
                if c in unauth:
                    del_indexs.append(i)
            # 删除一个元素，下一个待删除元素-n(n=1,2,3...)
            del_indexs.sort()
            plus = 0
            for i in del_indexs:
                del origin_columns[i - plus]
                plus += 1
            # 字段:原始 = columns:origin_columns
    return ''


def extract_tables_real_name(sql):
    # 提取表名列表
    stream = extract_from_part_table(sqlparse.parse(sql)[0])
    return list(extract_table_identifiers_table(stream))


def extract_from_part_table(parsed):
    from_seen = False
    for item in parsed.tokens:
        if item.value.upper().find('WHERE') != -1:
            break
        if item.is_group:
            for x in extract_from_part(item):
                yield x
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                if item.value.upper().find("JOIN") != -1:
                    continue
                elif item.value.upper() in ['ORDER', 'GROUP', 'BY', 'HAVING']:
                    from_seen = False
                    StopIteration
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers_table(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_real_name()
        elif isinstance(item, Identifier):
            yield item.get_real_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value


def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                raise StopIteration
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def obj2dict(item, keys=None):
    rt_dict = dict()
    if keys is None:
        keys = []
    if len(keys) == 0:
        item.__dict__.pop('_sa_instance_state', None)
        rt_dict = item.__dict__
        for (k, v) in rt_dict.items():
            if isinstance(v, datetime.datetime):
                rt_dict[k] = strftime(v)

    for name in keys:
        val = getattr(item, name)
        if isinstance(val, datetime.datetime):
            val = strftime(val)
        rt_dict[name] = val
    return rt_dict


def decimal2dict(item, keys=None):
    rt_dict = dict()
    if keys is None:
        keys = []
    for name in keys:
        val = getattr(item, name)
        if isinstance(val, datetime.datetime):
            val = strftime(val)
        if type(val) == decimal.Decimal:
            val = float(val)
        if val is None:
            val = '0.00%'
        rt_dict[name] = val
    return rt_dict


def is_Chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        return False


def import_to_excel(base_path, data, report_type):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = data['name'] + '_' + time + '.xlsx'
    report_path = base_path + file_name

    head = data["head"]
    datas = data["datas"]
    is_top = data["has_top"]

    workbook = xlsxwriter.Workbook(report_path)
    worksheet = workbook.add_worksheet()
    border_style = workbook.add_format()
    border_style.set_border(1)
    border_style.set_center_across()
    if is_top is False:
        row = 0
        col = 0
        if report_type == 104:
            column = head
        else:
            column = head[0]['items']
        f_column = copy.copy(column)
        for k, v in column.items():
            column[k] = v["sequence"]
        sort_columns = sorted(column.items(), key=lambda s: s[1])
        for sort_column in sort_columns:
            for ke, va in f_column.items():
                if ke == sort_column[0]:
                    worksheet.write(row, col, va["name"], border_style)
                    col += 1
        for data in datas:
            row += 1
            co = 0
            for sort_column in sort_columns:
                for key, value in data.items():
                    if key == sort_column[0]:
                        worksheet.write(row, co, value, border_style)
                        co += 1
    else:
        row = 0
        col = 0
        columns = head
        # merge_range(first_row, first_col, last_row, last_col, data[, cell_format])
        top_names = []
        dic_top = {}
        sort_columns = {}
        sort_columns_k = {}
        for column in columns:
            len_dic_top = {}
            j = len(column["items"])
            ke = column["top_name"]
            for (k, v) in column["items"].items():
                ve = v["sequence"]
                break
            for (k, v) in column["items"].items():
                sort_columns[v["name"]] = v["sequence"]
                sort_columns_k[k] = v["sequence"]
            len_dic_top[ke] = j
            dic_top[ke] = ve
            top_names.append(len_dic_top)
        t_sort_columns = sorted(sort_columns.items(), key=lambda s: s[1])
        k_sort_columns = sorted(sort_columns_k.items(), key=lambda s: s[1])
        # print(t_sort_columns)
        # print(top_names)
        # print(dic_top)
        sort_dic_tops = sorted(dic_top.items(), key=lambda s: s[1])
        # print(sort_dic_tops)
        for sort_dic_top in sort_dic_tops:
            for top_name in top_names:
                for key, value in top_name.items():
                    if sort_dic_top[0] == key:
                        worksheet.merge_range(row, col, row, col + value - 1,
                                              key, border_style)
                        col += value
        row = 1
        col = 0
        for t_sort_column in t_sort_columns:
            worksheet.write(row, col, t_sort_column[0], border_style)
            col += 1

        for data in datas:
            row += 1
            co = 0
            for k_sort_column in k_sort_columns:
                for key, value in data.items():
                    if key == k_sort_column[0]:
                        worksheet.write(row, co, value, border_style)
                        co += 1

    workbook.close()
    return file_name
