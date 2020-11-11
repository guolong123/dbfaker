from dbfaker.common.setting import get_yaml
import jinja2
import json
import copy
from dbfaker.common.logger import log
from dbfaker.common.database import Database
from tqdm import tqdm
import sys


class GeneratorField():
    def __init__(self, faker, meta, connect=None):
        self.faker = faker
        self.meta_data = get_yaml(meta)
        self.db = Database(db_session=connect) if connect else None
        self.all_package = {}
        self.env_data = {'faker': faker, 'env': {}, }
        self.field_data = {}
        self.extraction_data = {}
        self.log = log
        self.sqls = []
        self.error_data = {}

    def start(self):
        self._env()
        self._tables_handle()
        self.extraction()
        self._error_handle()
        self.data2sql()

    def import_package(self):
        self._import_package()

    def _import_package(self):
        """
        动态导包
        """
        if isinstance(__builtins__, dict):
            self.all_package.update(__builtins__)
        else:
            self.all_package.update(__builtins__.__dict__)
        packages = self.meta_data.get('package')
        if not packages:
            return
        for i in packages:
            try:
                self.all_package[i] = __import__(i)
            except ModuleNotFoundError:
                self.log.e('import package {} failed'.format(i))

    def _env(self):
        """
        环境变量预处理
        :param condition:
        :return:
        """
        self.env_data.update(self.all_package)
        env = self.meta_data.get('env')
        if not env:
            return
        self._field_handle(env_key='env', **env)

    def dict_resolve(self, data: dict):
        """
        递归将字典的value使用模板格式化
        :param data:
        :return:
        """
        if not isinstance(data, dict) and isinstance(data, str):
            return self._template_render(data)
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    self.dict_resolve(value)
                elif isinstance(value, str):
                    value = self._template_render(value)
                data[key] = value
        return data

    def _field_handle(self, env_key=None, max_number=1, **kwargs):
        result = []
        i = 0
        while i < max_number:
            data = {}
            for key, value in copy.deepcopy(kwargs).items():
                try:
                    _value = self.dict_resolve(value)
                    if not isinstance(value, dict):
                        _data = {key: _value}
                    elif 'engine' not in _value:
                        _data = {key: self._field_handle(**_value)}
                    else:
                        _data = {key: self._gen_field(**_value)}
                    data.update(_data)
                except jinja2.exceptions.UndefinedError:
                    if env_key not in self.error_data:
                        self.error_data[env_key] = {}
                    self.error_data[env_key].update({key: value})
                    continue
                if env_key:
                    if env_key not in self.env_data:
                        self.env_data[env_key] = {}
                    self.env_data[env_key].update(data)
            result.append(data)
            i += 1
        return result

    def _tables_handle(self):
        for tables in self.meta_data.get('tables'):
            table_name = tables.get("table")
            columns = tables.get('columns')
            max_number = tables.get('more', {}).get("max_number") or tables.get("max_number", 1)
            if isinstance(max_number, str):
                max_number = int(self._template_render(max_number))
            if not isinstance(columns, dict):
                raise TypeError("数据类型错误，此版本不再兼容老的yml格式，"
                                "请使用\"table2yml ymlcov xxx.yml\"来调整yml文件格式, "
                                "或将dbfaker版本降至0.0.5b1021.post2。")

            self.field_data[table_name] = self._field_handle(env_key=table_name, max_number=max_number, **columns)

    def extraction(self):
        extraction_metas = self.meta_data.get('extraction')
        if not extraction_metas:
            return
        self.extraction_data = self._field_handle(env_key='extraction', **extraction_metas)
        self.log.i('extraction data: {}'.format(self.extraction_data))
        return self.extraction_data

    def _error_handle(self):
        for table, field in self.error_data.items():
            self._field_handle(env_key=table, **field)

    def data2sql(self, datas=None):
        if not datas and isinstance(self.field_data, dict):
            datas = copy.deepcopy(self.field_data)

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

    def _gen_field(self, **kwargs):
        engine = kwargs.get('engine')
        rule = kwargs.get('rule')

        if isinstance(rule, str):
            rule = json.loads(self._template_render(rule))
        faker = self.faker
        if not engine:
            return
        if '.' not in engine:
            engine = "faker.{engine}".format(engine=engine)
        if "(" in engine and ")" in engine:
            r = eval(engine)
        else:
            if isinstance(rule, list):
                r = eval("{engine}(*{rule})".format(engine=engine, rule=rule))
            elif isinstance(rule, dict):
                r = eval("{engine}(**{rule})".format(engine=engine, rule=rule))
            elif rule is None:
                r = eval("{engine}()".format(engine=engine))
            else:
                raise Exception('rule type must be dictionary or list！')
        return r

    def _template_render(self, s, env=None):
        """
        jinja2模板渲染
        """
        source_type = type(s)
        if isinstance(s, (list, dict)):
            s = json.dumps(s).replace('\\\"', "'")
        tp = jinja2.Template(s)
        if isinstance(env, dict):
            self.all_package.update(env)
        tp.globals.update(self.all_package)
        r = tp.render(**self.env_data)
        if source_type in [list, dict]:
            r = json.loads(r)
        return r

    def save(self, output=None):
        if not output:
            return
        f = open(output, 'w')
        f.write('\n'.join(self.sqls))
        f.close()
