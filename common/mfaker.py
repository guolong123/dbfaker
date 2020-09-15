from faker import Faker
from faker.providers.date_time import Provider
import random
from datetime import timedelta
from dateutil.tz import tzutc
from faker.utils.datetime_safe import datetime
import uuid
from common.logger import log
import os
import re
import time
from common.setting import check_path
from common.mysqldb import Database
import pypinyin

faker = Faker(locale='zh_CN')



class MFaker(Provider):
    def __init__(self, offset=0, connect=None):
        super().__init__(faker)
        self.log = log
        self.db = None
        if connect:
            self.db = Database(connect)
        self.offset = offset

    def hans2pinyin(self, hans, style='A'):
        """
        汉字转拼音
        :param hans: 汉字
        :param style: 返回首字母还是全拼， A：全拼； F：首字母
        :return:
        """

        if style.upper() == 'F':
            return ''.join(pypinyin.lazy_pinyin(hans=hans, style=pypinyin.Style.FIRST_LETTER))
        else:
            return ''.join(pypinyin.lazy_pinyin(hans=hans))

    def eq(self, value=None):
        return value

    def choice(self, value):
        return random.choice(value)

    def choice_file(self, path, file_match=None, recursion=False, number=1):
        """
        指定目录寻找匹配规则的文件
        :param path:
        :param file_match:
        :param recursion:
        :return:
        """
        file_list = list(os.walk(check_path(path), ))
        if not file_list:
            # print(f'指定目录不存在“{file_match}”的文件')
            return
        if not recursion:
            file_list = file_list[0][-1]
            result = [os.path.abspath(s.string) for s in [re.match(file_match, x) for x in file_list] if s]
        else:
            result = []
            for k in list(zip(*file_list))[-1]:
                result += k
            result = [os.path.abspath(s.string) for s in [re.match(file_match, x) for x in result] if s]
        if len(result) < number:
            return result
        else:
            rs = []
            for i in range(number):
                rs.append(random.choice(result))
            return rs

    def uuid(self, underline=True):
        uid = str(uuid.uuid4())
        if underline:
            uid = uid.replace("-", '')
        return uid

    def from_db(self, sql, choice_method='random', key=None):
        """
        从数据库中查数据
        :param sql: 查询语句
        :param choice_method: 对返回多个值时的处理方式，random： 随机取一个， first：取第一个，其它：返回整个list
        :param key: 当key存在时，将从返回数据键值对中取键为“key”的值
        :param tag:
        :return:
        """
        if not self.db:
            self.log.w('未指定数据库连接引擎，无法从数据库查询数据')
            return
        result = self.db.select3(sql)
        if not result:
            return
        if key:
            result = [i[key] for i in result]
        if choice_method == 'random':
            result = random.choice(result)
        elif choice_method == 'first':
            result = result[0]
        return result

    def from_db_yield(self, sql, key=None):
        """
        从数据库中查数据
        :param sql: 查询语句
        :param choice_method: 对返回多个值时的处理方式，random： 随机取一个， first：取第一个，其它：返回整个list
        :param key: 当key存在时，将从返回数据键值对中取键为“key”的值
        :return:
        """
        if not self.db:
            self.log.w('未指定数据库连接引擎，无法从数据库查询数据')
            return
        result = self.db.select3(sql)
        if key:
            result = [i[key] for i in result]
        for i in result:
            yield i

    def date_time_between(self, start_date=None, end_date=None, tzinfo=None, offset=None, format=None):
        start_date = self._parse_date_time(start_date, tzinfo=tzinfo)
        end_date = self._parse_date_time(end_date, tzinfo=tzinfo)
        if not offset:
            offset = self.offset * 24 * 60 * 60
        else:
            offset = int(offset) * 24 * 60 * 60

        if end_date - start_date <= 1:
            ts = start_date + self.generator.random.random() - offset
        else:
            ts = self.generator.random.randint(start_date, end_date) - offset

        if tzinfo is None:
            result = datetime(1970, 1, 1, tzinfo=tzinfo) + timedelta(seconds=ts)
        else:
            result = (
                    datetime(1970, 1, 1, tzinfo=tzutc()) + timedelta(seconds=ts)
            ).astimezone(tzinfo)
        if format:
            result = result.strftime(format)
        return result

    def date_time_subtraction(self, start_date, sub_time, format=None, approximate_time=True):
        """
        指定开始时间点，与过去时间，计算结果时间，按照指定的格式返回
        :param start_date:
        :param sub_time:
        :param format:
        :param approximate_time: 是否返回浮动的时间（为Ｔｒｕｅ时将对sub_time时间进行随机正负一倍以内来返回）
        :return:
        """
        if isinstance(start_date, str) and format:
            start_date = datetime.strptime(start_date, format)
        elif isinstance(start_date, int):
            start_date = datetime.utcfromtimestamp(start_date)
        sub_time = self._parse_date_string(sub_time)
        key, value = list(sub_time.items())[0]
        appr_value = value + value*random.uniform(-1,1)
        if approximate_time:
            sub_time.update({key: appr_value})
        sub_time1 = timedelta(**sub_time)
        end_date = start_date + sub_time1
        return end_date.strftime(format)

    def now(self, format=None):
        """
        返回当前时间，format参数存在时按照format参数指定的时间格式进行返回，
        否则返回时间戳
        :param format: 格式化时间格式 %Y-%m-%d %H:%M:%S
        :return:
        """
        if format:
            r = datetime.now().strftime(format)
        else:
            r = int(time.time() * 1000)
        return r

    def weights_randint(self, *args):
        result = []
        for d in args:
            _weights = d.get('weights')
            value = d.get('value')
            n = 10
            while _weights < 1:
                _weights = int(_weights * n)
            for i in range(_weights):
                result.append(random.randint(*value))
        result = random.choice(result)
        return result

    def weights_randfloat(self, *args, round_num=2):
        """
        权重计算
        :param args:
        :param round_num:
        :return:
        """
        result = []
        for d in args:
            _weights = d.get('weight')
            value = d.get('value')
            if d.get("round_num"):
                round_num = d.get("round_num")
            n = 10
            while _weights < 1:
                _weights = int(_weights * n)
            for i in range(_weights):
                result.append(round(random.uniform(*value), round_num))
        result = random.choice(result)
        return result

    def weights_choice(self, *args):
        """
        权重选择
        :param args:
        :return:
        """
        values = []
        for d in args:
            weights = d.get('weight')
            value = d.get('value')
            if weights < 1:
                weights = int(weights * 100 / len(value))
            for i in value:
                values += [i] * weights
        result = random.choice(values)
        return result

    def multi_choice(self, value, splits="|", rand_number=None):
        """
        从指定的列表中随机选择多个，使用拼接字符拼起来返回
        :param value:
        :param splits:
        :return:
        """
        if rand_number and rand_number < len(value):
            rand_number = rand_number
        else:
            rand_number = random.randint(0, len(value))
        return splits.join([str(i) for i in random.sample(value, rand_number)])

    def randint(self, value):
        return random.randint(*value)

    def randfloat(self, value, round_num=2):
        return round(random.uniform(*value), round_num)

    def gen_data(self, engine, rule):
        if not engine:
            return
        if isinstance(rule, list):
            r = eval(engine + "(*{})".format(rule), )
        elif isinstance(rule, dict):
            r = eval(engine + "(**{})".format(rule), )
        elif rule is None:
            r = eval(engine + "()")
        else:
            raise Exception('rule type need be dict or list!')
        return r

    @staticmethod
    def order(value):
        for i in value:
            yield i


if __name__ == '__main__':
    # print(weights_randint([{"value": [-50, 0], "weights": 0.7}, {"value": [1, 100], "weights": 0.1}]))
    # print(weights_choice([{"value": ['01','02', '03', '04', '05', '06', '07', '08', '09', '10', '11'], "weights": 1}]))
    # print(weights_randfloat(*[{'value': [0, 1], 'weights': 1}]))
    # a = order([1,2,3])
    # print(a.__next__())
    pass
