# -*- encoding: utf-8 -*-
from dbfaker.utils.gendata import GeneratorField
import sys
import argparse
from dbfaker.utils.constant import __version__
from dbfaker.utils.faker_date_time import Provider as DateTimeProvider
from dbfaker.utils.faker_tool import Provider as ToolProvider
from faker import Faker
from dbfaker.utils.generator import MGenerator
from tqdm import tqdm
from dbfaker.utils.init_project import scaffold
import os
import importlib

faker = Faker(locale='zh_CN', generator=MGenerator(locale='zh_CN'))


def loop(meta_file, number=1, insert=False, connect=None, output=None, _print=True, **kwargs):
    handler = GeneratorField(faker, meta_file, connect, )
    handler.import_package()
    for i in tqdm(range(number), unit='组'):
        sys.stdout.flush()
        handler.start()
    if insert:
        handler.insert2db()
    if output:
        handler.save(output=output)
    if _print:
        [print(i) for i in handler.sqls]

    print('执行完成，共生成{number}组数据'.format(number=number))


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='通过ｙｍｌ格式的描述文件来生成数据')
    parser.add_argument('meta_file', nargs='?', action='store',
                        help='yml文件所在路径')
    parser.add_argument('-n', '--number', nargs='?', action='store', default=1,
                        help='生成数据数量', type=int)
    parser.add_argument('-i', '--insert', action='store_true', help='是否插入到数据库')
    parser.add_argument('-c', '--connect', nargs='?', action='store',
                        help='数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')

    parser.add_argument('-o', '--output', nargs='?', action='store',
                        help='指定文件名，输出内容到文件')
    parser.add_argument('-p', '--_print', action='store_true', help='是否打印到控制台')
    parser.add_argument('--project_name', action='store', help='初始化项目时的项目名称', default='dbfaker-project')
    args = parser.parse_args()
    if not args.meta_file:
        print('You must supply meta_file\n')
        parser.print_help()
        exit(0)

    if args.meta_file == 'init':
        scaffold(project_name=args.project_name)
        exit(0)

    if args.insert and not args.connect:
        print('You must supply connect\n')
        parser.print_help()
        exit(0)

    return args


def import_module(module_path='script'):
    if not os.path.exists(module_path):
        return
    pys = [x for x in list(os.walk(module_path))[0][-1] if x.endswith(".py")]
    modules = []
    for py in pys:
        module = importlib.import_module('{}.{}'.format(module_path, py.split(".")[0]))
        for class_name in dir(module):
            provider = getattr(module, class_name)
            if isinstance(provider, type):
                modules.append(provider)
    return modules


def run():
    cur_dir = os.path.abspath(os.curdir)
    sys.path.append(cur_dir)
    args = parse_args()
    faker.add_provider(DateTimeProvider, offset=0)
    faker.add_provider(ToolProvider, connect=args.__dict__.get("connect"))
    modules = import_module()
    if modules:
        for module in modules:
            faker.add_provider(module)
    loop(**args.__dict__)


if __name__ == '__main__':
    run()
