from utils.gendata import GenData
import sys
import argparse
from utils.constant import __version__
from utils.faker_date_time import Provider as DateTimeProvider
from utils.faker_tool import Provider as ToolProvider
from faker import Faker
from utils.generator import MGenerator

faker = Faker(locale='zh_CN', generator=MGenerator(locale='zh_CN'))

def loop(meta_file, number=1, insert=False, connect=None, output=None):
    n = 0

    sql_words = []
    while n < number:
        handler = GenData(faker, meta_file, connect)
        mock_data = handler.pre()
        for d in mock_data:
            sqls = handler.dict2sql(d)
            for sql in sqls:
                sql_words.append(handler.insert2db(sql, insert))
        n += 1
    if output:
        f = open(output, 'w')
        f.write('\n'.join(sql_words))
        f.close()
    else:
        [print(i) for i in sql_words]
    print(f'执行完成，共生成{number}组数据')


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='通过ｙｍｌ格式的描述文件来生成数据')
    parser.add_argument('meta_file', nargs='?', action='store',
                        help='yml文件所在路径')
    parser.add_argument('-n', '--number', nargs='?', action='store', default=1,
                        help='生成数据数量',type=int)
    parser.add_argument('-i', '--insert', action='store_true', help='是否插入到数据库')
    parser.add_argument('-c', '--connect', nargs='?', action='store',
                        help='数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')

    parser.add_argument('-o', '--output', nargs='?', action='store',
                        help='数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')
    args = parser.parse_args()
    if not args.meta_file:
        print('You must supply meta_file\n')
        parser.print_help()
        exit(0)

    if args.insert and not args.connect:
        print('You must supply connect\n')
        parser.print_help()
        exit(0)

    return args



if __name__ == '__main__':
    args = parse_args()
    faker.add_provider(DateTimeProvider, offset=0)
    faker.add_provider(ToolProvider, connect=args.__dict__.get("connect"))
    # add_provider(faker, DateTimeProvider, offset=0)
    # add_provider(faker, ToolProvider, connect=args.__dict__.get("connect"))
    loop(**args.__dict__)

