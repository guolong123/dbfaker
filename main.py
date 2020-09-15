from utils.gendata import GenData
import sys
import argparse
from utils.constant import __version__
from common.mfaker import MFaker, faker

def loop(meta_file, number=1, insert=False, connect=None):
    n = 0
    while n < number:
        handler = GenData(meta_file, connect, faker)
        mock_data = handler.pre()
        for d in mock_data:
            sqls = handler.dict2sql(d)
            for sql in sqls:
                handler.insert2db(sql, insert)
        print('\n')
        n += 1


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='通过ｙｍｌ格式的描述文件来生成数据')
    parser.add_argument('meta_file', nargs='?', action='store',
                        help='yml文件所在路径')
    parser.add_argument('--number', nargs='?', action='store', default=1,
                        help='生成数据数量',type=int)
    parser.add_argument('--insert', nargs='?', action='store', help='是否插入到数据库')
    parser.add_argument('--connect', nargs='?', action='store',
                        help='数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')
    args = parser.parse_args()
    if not args.meta_file:
        print('You must supply meta_file\n')
        parser.print_help()
        exit(0)
    return args


if __name__ == '__main__':
    args = parse_args()
    faker.add_provider(MFaker(connect=args.__dict__.get('connect')))
    loop(**args.__dict__)

