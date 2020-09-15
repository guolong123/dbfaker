import json
import yaml
from common.mysqldb import Database
from nsqlparse.mysql_create_table_yacc import parser
import sys
import os
from utils.constant import __version__
import argparse

sys.modules["MySQLDB"] = sys.modules["_mysql"] = sys.modules["pymysql"]


def table_name_to_table_building_statement(db_session, tables):
    table_words = ';\n'.join([db_session.query_table(s) for s in tables]) + ';'
    print(table_words)
    return table_words


def start(connect, table_names=None,
          sql_file=None, output=None, **kwargs):
    if table_names:
        if "," in table_names:
            tables = table_names.split(",")
        else:
            tables = [table_names]
        file_name = '_'.join(tables) + '_meta.yml'
        session = Database(connect)
        table_building_statement = table_name_to_table_building_statement(session, tables)
    else:
        file_name = os.path.split(sql_file)[1] + '_meta.yml'
        with open(sql_file)as f:
            table_building_statement = f.read()

    result = {
        "condition": None,
        'tables': None,
    }

    r = parser.parse(table_building_statement)
    for i in r:
        i.pop("keys") if 'keys' in i else None
        i.pop("row_format") if 'row_format' in i else None
        i.pop("engine") if 'engine' in i else None
        i.pop("default_charset") if 'default_charset' in i else None
        for j in i['columns']:
            j.pop("type") if 'type' in j else None
            j.pop("length") if 'length' in j else None
            j.pop("not_null") if 'not_null' in j else None
            j.pop("default") if 'default' in j else None
            j['engine'] = None
            j['rule'] = None
    result.update({"tables": r})
    if not output:
        output = file_name
    f = open(output, 'w')
    f.write('''# 请完善此文件中每个字段的生成规则"engine/rule/tag"
# 规则说明：
# "engine": 字段生成的方法，在工具类中需包含此方法的引用；
# "rule"： "engine"方法中接收的参数
# "tag"： 接收一个变量名，在字段生成后将结果赋值给这个变量名。可在后续的字段进行引用

''' + yaml.dump(result, encoding='utf-8', allow_unicode=True, default_flow_style=False).decode())
    f.close()
    print(f'table转ymal文件成功，文件路径：{os.path.abspath(output)}')


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='数据库表转数据生成yaml文件格式工具')
    parser.add_argument('type', nargs='?', action='store', default='table_name',
                        help='数据来源，table_name： 通过输入表名与数据库链接方式，在数据库中获取数据库建表语句；\n table_statement: 指定数据库建表语句的sql文件路径')
    parser.add_argument('--connect', nargs='?', action='store',
                        help='数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')
    parser.add_argument('--table_names', nargs='?', action='store', help='数据库表，多个表以“,”分割')
    parser.add_argument('--sql_file', nargs='?', action='store', help='数据库建表语句的sql文件路径')
    parser.add_argument('--output', nargs='?', action='store', default=None, help='输出文件名，默认为数据库表名+meta.yml')
    args = parser.parse_args()

    if args.type == 'table_name' and (not args.connect or not args.table_names):
        print('You must supply a connect and table_names\n')
        parser.print_help()
        exit(0)

    if args.type == 'table_statement' and not args.sql_file:
        print('You must supply a sql_file\n')
        parser.print_help()
        exit(0)

    return args


if __name__ == '__main__':
    args = parse_args()
    start(**args.__dict__)
