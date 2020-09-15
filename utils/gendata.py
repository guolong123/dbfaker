from common.setting import get_yaml
import jinja2
from common.mfaker import faker as fk
import json
import copy
from common.logger import log
from common.mysqldb import Database
import os
import sys


class GenData:
    def __init__(self, meta=None, connect=None, faker=None):
        self.all_package = {}
        self.pre_data = {}
        self.log = log
        if not faker:
            self.faker = fk
        else:
            self.faker = faker
        if connect:
            self.db = Database(connect)
        else:
            self.db = None
        self.meta = get_yaml(meta)
        self.mock_data = []
        self._import_package()
        self.env()

    def _import_package(self):
        self.all_package.update(__builtins__)
        packages = self.meta.get('package')
        if not packages:
            return
        for i in packages:
            try:
                self.all_package[i] = __import__(i)
            except ModuleNotFoundError:
                pass

    def env(self):
        """
        环境变量预处理
        :param condition:
        :return:
        """
        self.pre_data['env'] = {}
        condition = self.meta.get('env')
        if not condition:
            return
        for i, j in condition.items():
            engine = j.get("engine")
            rule = j.get("rule")
            result = self.faker.gen_data(engine, rule)
            self.pre_data['env'][i] = result

    def field(self, columns):
        result = {}
        pre_data = {}
        table_name = columns.get("table")
        pre_data[table_name] = {}
        for field in columns.get('columns'):
            field_column = field.get('column')
            field_comment = field.get('comment')
            field_engine = field.get('engine')
            field_rule = field.get("rule")
            if field_rule:
                _rule = json.dumps(field.get("rule"))
                _rule = _rule.replace('\\\"', "'")
                tp = jinja2.Template(_rule)
                tp.globals.update(self.all_package)
                field_rule = json.loads(tp.render(**self.pre_data, **pre_data))
            _r = self.faker.gen_data(field_engine, field_rule)
            result[field_column] = _r
            pre_data[table_name][field_column] = _r
        self.pre_data.update(pre_data)

        return result

    def more_field(self, columns, max_cnt=1):
        results = []
        result = {}
        table_name = columns.get("table")
        n = 0
        while n < max_cnt:
            try:
                for field in columns.get('columns'):
                    field_column = field.get('column')
                    field_comment = field.get('comment')
                    field_engine = field.get('engine')
                    tp = jinja2.Template(json.dumps(field.get("rule")), undefined=jinja2.StrictUndefined)
                    tp.globals.update(self.all_package)
                    field_rule = json.loads(tp.render(**self.pre_data))
                    _r = self.faker.gen_data(field_engine, field_rule)
                    result[field_column] = _r
            except jinja2.exceptions.UndefinedError:
                break
            results.append(copy.deepcopy(result))
            n += 1
        self.pre_data[table_name] = results
        return results

    def pre(self):
        fields = self.meta.get('tables')
        for columns in fields:
            d = {}
            table_name = columns.get("table")
            d['comment'] = columns.get("comment")
            more = columns.get('more')
            d['table_name'] = table_name
            if not more:
                d['fields'] = self.field(columns)
            else:
                max_cnt = more.get("max_cnt", 1)
                d['fields'] = self.more_field(columns=columns, max_cnt=max_cnt)
            self.mock_data.append(d)
        return self.mock_data

    def dict2sql(self, data):
        def d2s(table, fields):
            ls = [(k, fields[k]) for k in fields if fields[k]]
            sql = f"insert into {table} set " + ', '.join([i[0] + "=%r" % i[1] for i in ls]) + ';'
            return sql

        table = data.get("table_name")
        fields = data.get("fields")
        sqls = []
        if isinstance(fields, list):
            for i in fields:
                sql = d2s(table, i)
                sqls.append(sql)
        elif isinstance(fields, dict):
            sql = d2s(table, fields)
            sqls.append(sql)
        return sqls

    def insert2db(self, sql, insert=True):
        print(sql)
        if self.db and insert:
            self.db.query(sql)


if __name__ == '__main__':

    g = GenData(meta='../data/ecg_report_meta.yml')
    g.condition()
    ds = g.pre()
    for d in ds:
        g.dict2sql(data=d)
