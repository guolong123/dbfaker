import unittest
from utils.gendata import GenData
from common.setting import get_yaml


class MyTestCase(unittest.TestCase):
    handler = GenData()

    def test_gen_report(self):
        data = get_yaml('../data/ecg_report_meta.yml')
        self.handler.condition(data.get('condition'))
        self.handler.pre(data.get('tables'))
        # self.assertEqual(True, False)

    def test_gen_patient_info(self):
        data = get_yaml('../data/information_sick_meta.yml')
        self.handler.condition(data.get('condition'))
        datas = self.handler.pre(data.get('tables'))
        for d in datas:
            sqls = self.handler.dict2sql(d)
            for sql in sqls:
                self.handler.insert2db(sql)


if __name__ == '__main__':
    unittest.main()
