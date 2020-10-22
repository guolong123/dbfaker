import unittest
import os
import sqlite3


class MyTestCase(unittest.TestCase):
    os.chdir('..')

    def test_001(self):
        print(os.popen('dbfaker data/test.yml -o test.sql -n 100').read())
        s = list(os.walk('.'))
        self.assertIn('test.sql', s[0][-1])
        os.remove('test.sql')

    def test_002(self):
        NUMBER = 10  # 生成数据数量
        db = sqlite3.connect('data/test.db')
        cur = db.cursor()
        cur.execute('select count(1) from stu')
        start_num = cur.fetchall()[0][0]
        print(os.popen('dbfaker data/test.yml -i --connect sqlite:///data/test.db -n {}'.format(NUMBER)).read())
        cur.execute('select count(1) from stu')
        end_num = cur.fetchall()[0][0]
        self.assertEqual(end_num-start_num, NUMBER)

if __name__ == '__main__':
    unittest.main()
