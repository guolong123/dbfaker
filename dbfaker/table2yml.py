import yaml
from dbfaker.common.database import Database
import sys
import os
from dbfaker.utils.constant import __version__
import argparse
from dbfaker.common.setting import get_yaml
from dbfaker.nsqlparse.mysql_create_table_yacc import parser


def table_name_to_table_building_statement(db_session, tables):
    table_words = ';\n'.join([db_session.query_table(s) for s in tables]) + ';'
    print(table_words)
    return table_words


def old_yml_to_new(old_yml_file, hide_comment=False):
    data = get_yaml(old_yml_file)
    for table in data['tables']:
        column_dict = {}
        for columns in table['columns']:
            if hide_comment and 'comment' in columns:
                columns.pop("comment")
            column_dict[columns.pop("column")] = columns
        table['columns'] = column_dict
        if hide_comment and 'comment' in table:
            table.pop("comment")

    base_path, base_file = os.path.split(old_yml_file)[0:2]
    new_file = base_file.split(".")[0] + '_new' + '.yml'
    new_file_path = os.path.join(base_path, new_file)
    with open(new_file_path, 'w') as f:
        f.write(
            yaml.dump(data, encoding='utf-8', allow_unicode=True, default_flow_style=False, sort_keys=False).decode())
    print('数据转换成功；新文件地址： {}'.format(new_file_path))


def start(type, **kwargs):
    if type == 'table_name':
        table_names = kwargs.get('table_names')
        connect = kwargs.get('connect')

        if table_names:
            if "," in table_names:
                tables = table_names.split(",")
            else:
                tables = [table_names]
            file_name = '_'.join(tables) + '_meta.yml'
            session = Database(connect)
            table_building_statement = table_name_to_table_building_statement(session, tables)
        else:
            raise ValueError("table_names can not be null!")
    elif type == 'table_statement':
        sql_file = kwargs.get('sql_file')
        file_name = os.path.split(sql_file)[1] + '_meta.yml'
        with open(sql_file, encoding='utf-8')as f:
            table_building_statement = f.read()

    elif type == 'ymlcov':
        old_yml_to_new(kwargs.get('yml_file'), hide_comment=kwargs.get('hide_comment'))
        return

    else:
        raise TypeError("type must be \"table_statement\" or \"table_name\" or \"ymlcov\"")

    result = {
        "package": [],
        "env": {},
        'tables': [],
        "extraction": {}

    }

    r = parser.parse(table_building_statement)
    hide_comment = kwargs.get('hide_comment')
    for i in r:
        if hide_comment:
            table_obj = {'table': i.get("table"), "columns": {}}
        else:
            table_obj = {'table': i.get("table"), 'comment': i.get("comment"), "columns": {}}
        for j in i['columns']:
            if hide_comment:
                table_obj['columns'][j.get("column")] = {'engine': None}
            else:
                table_obj['columns'][j.get("column")] = {'comment': j.get("comment"), 'engine': None}

        result['tables'].append(table_obj)
    output = kwargs.get('output')
    if not output:
        output = file_name
        if os.path.exists('data'):
            output = os.path.join('data', output)
    f = open(output, 'w', encoding='utf-8')
    f.write('''# 请完善此文件中每个字段的生成规则
# 规则说明：
# package: 动态导包，在下方字段使用了jinja2模板且在模板语法中使用了非Python基础库时需要在此动态声明导入需要的包;使用示例:
# package:
#  - datetime  # 引入datetime包，可在后续的jinja2模板中使用
#  - os

# env: 可在此处预生成环境变量，给下方字段生成时引用；描述方式如下：
# env:
#  name:  # 全局变量名称
#    engine: eq  # 生成规则方法，与下面的字段生成方法一样。也可不需要下方的rule参数，直接在engine后面写参数：例如：eq('test')
#    rule:  # "engine"方法中接收的参数; 当engine中包含"()"时此参数将不会生效。
#      value: 'test'  

# tables： 该字段描述了表字段的生成规则，需要填写数据库字段中的engine与rule字段，为空时数据库字段也为空；示例(给数据库中t_sys_user表中age字段生成从40到80的随机数)：
# tables:
# - table: t_sys_user
#   comment: 用户表
#   columns:
#     age:  # 数据库中字段名
#       comment: '年龄'  # 字段备注信息
#       engine: randint  # 生成字段值调用的方法，必须是faker库中存在或者自行注册到faker库中的方法。也可不需要下方的rule参数，直接在engine后面写参数：例如：randint(value=[40,80])
#       rule:  # 当engine中包含"()"时此参数将不会生效。
#          value: [40, 80]  # 上述方法中接收到的参数
       
# extraction： 该字段描述了需要从生成字段中提取哪些变量来返回，写自动化测试用例时可能会用到；举例：
# extraction：
#   user_name:
#     value: '{{ t_sys_user.name }}'  # 返回上面生成的用户姓名
#     default: '测试用户'  # 可指定默认值，在上述字段不存在或者为空时返回默认值
#   user_id:
#     value: '{{ t_sys_user.id }}'  


''' + yaml.dump(result, encoding='utf-8', allow_unicode=True, default_flow_style=False, sort_keys=False).decode())
    f.close()
    print('table转ymal文件成功，文件路径：{}'.format(os.path.abspath(output)))


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='数据库表转数据生成yaml文件格式工具')
    parser.add_argument('type', nargs='?', action='store', default='table_name',
                        help='操作： table_name： 通过输入表名与数据库链接方式，在数据库中获取数据库建表语句；\n table_statement: 指定数据库建表语句的sql文件路径 \n ymlcov: 将版本1.0.0以下的yml文件转换成当前版本')
    parser.add_argument('--connect', nargs='?', action='store',
                        help='数据库连接语法，例如：mysql+mysqldb://user:password@host/dbname')
    parser.add_argument('--table_names', nargs='?', action='store', help='数据库表，多个表以“,”分割')
    parser.add_argument('--sql_file', nargs='?', action='store', help='数据库建表语句的sql文件路径')
    parser.add_argument('--yml_file', nargs='?', action='store', help='要转换的yml文件路径（操作为ymlc时需要）')
    parser.add_argument('--output', nargs='?', action='store', default=None, help='输出文件名，默认为数据库表名+meta.yml')
    parser.add_argument('--hide_comment', action='store_true', help='不转换comment字段（可减少yml文件行数）')
    args = parser.parse_args()

    if args.type == 'table_name' and (not args.connect or not args.table_names):
        print('You must supply a connect and table_names\n')
        parser.print_help()
        exit(0)

    elif args.type == 'table_statement' and not args.sql_file:
        print('You must supply a sql_file\n')
        parser.print_help()
        exit(0)

    elif args.type == 'ymlcov' and not args.yml_file:
        print('You must supply a yml_file\n')
        parser.print_help()
        exit(0)

    return args


def main():
    args = parse_args()
    start(**args.__dict__)


if __name__ == '__main__':
    main()
