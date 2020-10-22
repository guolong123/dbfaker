import unittest
from dbfaker.utils.faker_tool import Provider
from faker import Faker
from dbfaker.utils.generator import MGenerator

mfaker = Faker(locale='zh_CN', generator=MGenerator(locale='zh_CN'))

# 测试连接地址为内部地址，外部访问将会失败。
mfaker.add_provider(Provider, connect='mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')

class MfakerTestCase(unittest.TestCase):
    mfaker = mfaker
    def test_uuid_1(self):
        uid = self.mfaker.uuid(underline=True)
        self.assertEqual(len(uid), 32)

    def test_uuid_2(self):
        uid = self.mfaker.uuid(underline=False)
        self.assertEqual(len(uid), 36)

    def test_uuid_3(self):
        uid = self.mfaker.uuid(underline=False)
        self.assertEqual(len(uid), 36)

    def test_from_db(self):
        db_result = self.mfaker.from_db(
            sql='select id from device_info where class_id=(select id from device_classify where serial=\'HL-ECG\')',
            choice_method='first', key='id')
        self.assertEqual(bool(db_result), True)

    def test_choice_file(self):
        self.mfaker.choice_file(path='.', file_match='.*?\.(png|jpg|bmp|PNG|JPG|BMP|py)$', recursion=True)
        self.mfaker.choice_file(path='../../', file_match='.*?\.(png|jpg|bmp|PNG|JPG|BMP|py)$', recursion=True, number=3)
        self.mfaker.choice_file(path='../../', file_match='.*?\.(png|jpg|bmp|PNG|JPG|BMP|py)$', recursion=False)

    def test_choice(self):
        data = [1,2,3,4,5,6,7,8]
        r = self.mfaker.choice(data)
        self.assertIn(r, data)

    def test_from_db_yield(self):
        result = self.mfaker.from_db_yield(
            sql="select id from report_detail_properties where name in ('QT', 'PR', 'QTC', 'RV5', 'HR', 'QRSaxis', 'R+S', 'QRS', 'P', 'SV1')",
            key='id')
        while 1:
            try:
                next(result)
            except StopIteration:
                break
        # self.assertEqual(len(r), 32)

if __name__ == '__main__':
    unittest.main()
