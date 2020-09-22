import unittest
import os



class MyTestCase(unittest.TestCase):
    os.chdir('..')

    def test_gen_report(self):
        print(os.popen('dbfaker data/test.yml -o test.sql -n 100').read())
        s = list(os.walk('.'))
        self.assertIn('test.sql', s[0][-1])

if __name__ == '__main__':
    unittest.main()
