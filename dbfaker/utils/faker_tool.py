from faker.providers import BaseProvider
import random
import uuid
from dbfaker.common.logger import log
import os
import re
import json
from dbfaker.common.setting import check_path
from dbfaker.common.database import Database
import pypinyin


class Provider(BaseProvider):
    def __init__(self, generator, connect=None):
        super().__init__(generator)
        self.log = log
        self.db = None
        if connect:
            self.db = Database(connect)

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
        """
        原样返回
        """
        return value

    def choice(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
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
            return
        if not recursion:
            file_list = file_list[0][-1]
            result = [os.path.abspath(s.string) for s in [re.match(file_match, x) for x in file_list] if s]
        else:
            result = []
            for k in list(zip(*file_list))[-1]:
                result += k
            result = [os.path.abspath(s.string) for s in [re.match(file_match, x) for x in result] if s]
        if len(result) > number:
            result = random.sample(result, number)
        return result

    def uuid(self, underline=True):
        """
        返回遗传32位随机字符串
        """
        uid = str(uuid.uuid4())
        if underline:
            uid = uid.replace("-", '')
        self.log.d('生成uuid： {}'.format(uid))
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

    def weights_randint(self, *args):
        """
        带权重的随机数，int型
        >> weights_randint({"weight": 0.8, "value": [1,2]}, {"weight": 0.2, "value": [3,4]})
        >> 1
        """
        result = []
        for d in args:
            _weights = d.get('weight')
            value = d.get('value')
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass

            n = 10
            while _weights < 1:
                _weights = int(_weights * n)
            for i in range(_weights):
                result.append(random.randint(*value))
        result = random.choice(result)
        return result

    def weights_randfloat(self, *args, round_num=2):
        """
        权重计算随机数float类型
        :param args:
        :param round_num:
        :return:
        """
        result = []
        for d in args:
            _weights = d.get('weight')
            value = d.get('value')
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass
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
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass
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
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        if not rand_number or rand_number > len(value):
            rand_number = random.randint(0, len(value))
        return splits.join([str(i) for i in random.sample(value, rand_number)])

    def randint(self, value: list):
        """
        从给定的数值范围内随机返回一个int数值
        """
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        return random.randint(*value)

    def randfloat(self, value: list, round_num=2):
        """
        从给定的数值范围内随机返回一个float数值
        """
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        return round(random.uniform(*value), round_num)


    @staticmethod
    def order(value, out_of_order=False):
        """
        返回一个列表生成器对象，使用next()来调用
        """
        if out_of_order and isinstance(value, list):
            value = list(set(value))
        for i in value:
            yield i

