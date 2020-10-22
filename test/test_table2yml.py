import unittest
import os

class MyTestCase(unittest.TestCase):
    os.chdir('..')
    def test_from_file(self):
        os.popen('table2yml table_statement --sql_file "data/test.sql" --output stu_meta.yml').read()
        s = list(os.walk('.'))
        self.assertIn('stu_meta.yml', s[0][-1])
        os.remove('stu_meta.yml')

    def test_from_db(self):
        os.popen('table2yml table_name --table_names "stu,course,choice_course" --connect sqlite:///data/test.db --output stu_meta.yml').read()
        s = list(os.walk('.'))
        self.assertIn('stu_meta.yml', s[0][-1])
        os.remove('stu_meta.yml')



if __name__ == '__main__':
    unittest.main()
