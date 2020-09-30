from faker.providers.date_time import Provider as DataTimeProvider
from datetime import timedelta, datetime
from dateutil.tz import tzutc
import random
import time


class Provider(DataTimeProvider):

    def __init__(self, generator, offset=0):
        super().__init__(generator)
        self.offset = offset

    def date_time_between(self, start_date=None, end_date=None, tzinfo=None, offset=None, format=None):
        """
        指定开始时间点，与过去时间，计算结果时间，按照指定的格式返回
        :param start_date: 随机时间范围的开始时间
        :param end_date: 随机时间范围的结束时间
        :param tzinfo: 时区设置
        :param offset: 时间偏移，示例： -2d，指的是在开始时间和结束时间中确定了某个时间点后再往前推2天。
        :param format: 返回的时间格式
        :return:
        """
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
        :param approximate_time: 是否返回浮动的时间（为true时将对sub_time时间进行随机正负一倍以内来返回）
        :return:
        """
        if isinstance(start_date, str) and format:
            start_date = datetime.strptime(start_date, format)
        elif isinstance(start_date, int):
            start_date = datetime.utcfromtimestamp(start_date)
        sub_time = self._parse_date_string(sub_time)
        key, value = list(sub_time.items())[0]
        appr_value = value + value * random.uniform(-1, 1)
        if approximate_time:
            sub_time.update({key: appr_value})
        sub_time1 = timedelta(**sub_time)
        end_date = start_date + sub_time1
        if format:
            return end_date.strftime(format)
        else:
            return end_date.second

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
