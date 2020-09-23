from dbfaker.common.setting import get_yaml
import jinja2
import json
import copy
from dbfaker.common.logger import log
from dbfaker.common.mysqldb import Database


class DataGenerator:
    def __init__(self, faker, meta, connect=None):
        self.all_package = {}
        self.pre_data = {}
        self.result_data = []
        self.log = log
        self.faker = faker
        self.sqls = []
        if connect:
            self.db = Database(connect)
        else:
            self.db = None
        self.meta = get_yaml(meta)

    def __call__(self, *args, **kwargs):
        self._import_package()
        self._env()
        self.mock_data()
        self.extraction()
        return self

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

    def _env(self):
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
            result = self._gen_data(engine, rule)
            self.pre_data['env'][i] = result

    def _field(self, columns):
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
                field_rule = json.loads(self._template_render(_rule))
            _r = self._gen_data(field_engine, field_rule)
            result[field_column] = _r
            pre_data[table_name][field_column] = _r
            self.pre_data.update(pre_data)
        return result

    def _template_render(self, s, env=None):
        """
        jinja2模板渲染
        """
        tp = jinja2.Template(s, undefined=jinja2.StrictUndefined)
        if isinstance(env, dict):
            self.all_package.update(env)
        tp.globals.update(self.all_package)
        r = tp.render(**self.pre_data)
        return r

    def _more_field(self, columns, max_cnt=1):
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
                    field_rule = json.loads(self._template_render(json.dumps(field.get("rule"))))
                    _r = self._gen_data(field_engine, field_rule)
                    result[field_column] = _r
            except jinja2.exceptions.UndefinedError:
                break
            results.append(copy.deepcopy(result))
            n += 1
        self.pre_data[table_name] = results
        return results

    def _gen_data(self, engine:str, rule):
        faker = self.faker
        if not engine:
            return
        if '.' not in engine:
            engine = f"faker.{engine}"
        if isinstance(rule, list):
            r = eval(f"{engine}(*{rule})")
        elif isinstance(rule, dict):
            r = eval(f"{engine}(**{rule})")
        elif rule is None:
            r = eval(f"{engine}()")
        else:
            raise Exception('rule type need be dict or list!')
        return r

    def mock_data(self):

        fields = self.meta.get('tables')
        for columns in fields:
            d = {}
            table_name = columns.get("table")
            # d['comment'] = columns.get("comment")
            more = columns.get('more')
            d['table_name'] = table_name
            if not more:
                d['fields'] = self._field(columns)
            else:
                max_cnt = more.get("max_number", 1)
                d['fields'] = self._more_field(columns=columns, max_cnt=max_cnt)
            self.result_data.append(d)
        return self.result_data

    def extraction(self):
        self.extraction_data = {}
        extraction_metas = self.meta.get('extraction')
        if not extraction_metas:
            return self.extraction_data
        for ext in extraction_metas:
            for key, values in ext.items():
                value = {'value': self._template_render(values.get('value', ''))}
                r_value = self._gen_data('eq', value)
                default = values.pop("default") if 'default' in values else None
                if not r_value:
                    r_value = default
                self.extraction_data[key] = r_value
        return self.extraction_data


    def dict2sql(self, datas=None):
        if not datas and isinstance(self.result_data, list):
            datas = self.result_data
        def d2s(table, fields):
            ls = [(k, fields[k]) for k in fields if fields[k]]
            sql = f"insert into {table} set " + ', '.join([i[0] + "=%r" % i[1] for i in ls]) + ';'
            return sql


        for data in datas:
            table = data.get("table_name")
            fields = data.get("fields")

            if isinstance(fields, list):
                for i in fields:
                    sql = d2s(table, i)
                    self.sqls.append(sql)
            elif isinstance(fields, dict):
                sql = d2s(table, fields)
                self.sqls.append(sql)
        return self.sqls

    def insert2db(self, sql=None):
        if not sql:
            return
        if self.db:
            self.db.query(sql)
        else:
            self.log.w('未指定数据库连接引擎，无法插入到数据库...')
