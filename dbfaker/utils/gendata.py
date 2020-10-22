from dbfaker.common.setting import get_yaml
import jinja2
import json
import copy
from dbfaker.common.logger import log
from dbfaker.common.database import Database
from tqdm import tqdm
import sys


class DataGenerator:
    def __init__(self, faker, meta, connect=None):
        self.all_package = {}
        self.pre_data = {}
        self.result_data = {}
        self.extraction_data = {}
        self.log = log
        self.error_fields = {}
        self.faker = faker
        self.sqls = []
        self.db = Database(connect) if connect else None
        self.meta = get_yaml(meta)

    def import_package(self):
        self._import_package()

    def start(self):
        self.result_data = {}
        self.extraction_data = {}
        self._env()
        self.mock_data()
        self.extraction()
        self._error_field()
        self.dict2sql()
        return self

    def save(self, output=None):
        if not output:
            return
        f = open(output, 'w')
        f.write('\n'.join(self.sqls))
        f.close()

    def _import_package(self):
        """
        动态导包
        """
        if isinstance(__builtins__, dict):
            self.all_package.update(__builtins__)
        else:
            self.all_package.update(__builtins__.__dict__)
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
        env = self.meta.get('env')
        if not env:
            return
        for i, j in env.items():
            engine = j.get("engine")
            rule = j.get("rule")
            rule = json.dumps(rule)
            result = self._gen_data(engine, rule)
            self.pre_data['env'][i] = result

    def _field(self, columns):
        result = {}
        pre_data = {}
        error_field = []
        table_name = columns.get("table")
        pre_data[table_name] = {}
        for field in columns.get('columns'):
            field_column = field.get('column')
            field_engine = field.get('engine')
            field_rule = field.get("rule")
            if field_rule:
                _rule = json.dumps(field.get("rule"))
                _rule = _rule.replace('\\\"', "'")
                try:
                    field_rule = json.loads(self._template_render(_rule))
                except jinja2.exceptions.UndefinedError as e:
                    error_field.append(field)
                    continue
            _r = self._gen_data(field_engine, field_rule)
            result[field_column] = _r
            pre_data[table_name][field_column] = _r
            if table_name not in self.pre_data:
                self.pre_data[table_name] = {}
            self.pre_data[table_name].update(pre_data[table_name])
            if error_field:
                # 记录表中出错的字段，在所有字段都生成后再次生成，解决因前面字段调用未生成字段时报错问题
                self.error_fields.update({'columns': error_field, 'table': table_name})
        return result

    def _more_field(self, columns, max_cnt=1):
        results = []
        result = {}
        table_name = columns.get("table")
        n = 0
        while n < max_cnt:
            try:
                for field in columns.get('columns'):
                    field_column = field.get('column')
                    field_engine = field.get('engine')
                    field_rule = json.loads(self._template_render(json.dumps(field.get("rule"))))
                    _r = self._gen_data(field_engine, field_rule)
                    result[field_column] = _r
            except jinja2.exceptions.UndefinedError as e:
                break
            results.append(copy.deepcopy(result))
            n += 1
        self.pre_data[table_name] = results
        return results

    def _error_field(self):
        """
        异常字段重新处理，解决引用的字段还未生成时造成的引用失败的问题
        """
        if not self.error_fields:
            return
        self.mock_data([self.error_fields])

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

    def _gen_data(self, engine: str, rule):
        if isinstance(rule, str):
            rule = json.loads(self._template_render(rule))
        faker = self.faker
        if not engine:
            return
        if '.' not in engine:
            engine = "faker.{engine}".format(engine=engine)
        if isinstance(rule, list):
            r = eval("{engine}(*{rule})".format(engine=engine, rule=rule))
        elif isinstance(rule, dict):
            r = eval("{engine}(**{rule})".format(engine=engine, rule=rule))
        elif rule is None:
            r = eval("{engine}()".format(engine=engine))
        else:
            raise Exception('rule type must be dictionary or list！')
        return r

    def mock_data(self, fields=None):

        if not fields:
            fields = self.meta.get('tables')
        for columns in fields:
            table_name = columns.get("table")
            more = columns.get('more')
            if not more:
                d = self._field(columns)
            else:
                max_cnt = more.get("max_number", 1)
                if isinstance(max_cnt, str):
                    max_cnt = int(self._template_render(max_cnt))
                d = self._more_field(columns=columns, max_cnt=max_cnt)
            if table_name not in self.result_data and not more:
                self.result_data[table_name] = {}
                self.result_data[table_name].update(d)
            elif table_name not in self.result_data:
                self.result_data[table_name] = d

        return self.result_data

    def extraction(self):
        extraction_metas = self.meta.get('extraction')
        if not extraction_metas:
            return self.extraction_data

        for key, values in extraction_metas.items():
            value = {'value': self._template_render(values.get('value', ''))}
            r_value = self._gen_data('eq', value)
            default = values.pop("default") if 'default' in values else None
            if not r_value:
                r_value = default
            self.extraction_data[key] = r_value
        return self.extraction_data

    def dict2sql(self, datas=None):
        if not datas and isinstance(self.result_data, dict):
            datas = copy.deepcopy(self.result_data)

        def gen_sql(table_name, data):
            """
            :param table_name: 表名称
            :param data: 字典对象 key为字段(要与数据库字段一样), value为插入值
            :return: 拼接好的sql语句
            """

            ls = [('`' + k + '`', v) for k, v in data.items() if v is not None]
            sentence = 'INSERT INTO `%s` (' % table_name + ','.join([i[0] for i in ls]) + \
                       ') VALUES (' + ','.join(repr(i[1]) for i in ls) + ');'
            return sentence

        for table, fields in datas.items():
            if isinstance(fields, list):
                for i in fields:
                    sql = gen_sql(table, i)
                    self.sqls.append(sql)
            elif isinstance(fields, dict):
                sql = gen_sql(table, fields)
                self.sqls.append(sql)
        return self.sqls

    def insert2db(self):
        self.log.i('开始插入数据至数据库')
        print('开始插入数据至数据库')
        if not self.db:
            self.log.w('未指定数据库连接引擎，无法插入到数据库...')
            return
        for sql in tqdm(self.sqls, unit='条'):
            sys.stdout.flush()
            self.db.query(sql)
        self.log.i('在数据库中插入了{}条数据'.format(len(self.sqls)))
        print('在数据库中插入了{}条数据'.format(len(self.sqls)))

