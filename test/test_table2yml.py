import unittest
import os

class MyTestCase(unittest.TestCase):
    os.chdir('..')
    def test_from_file(self):
        os.popen('table2yml table_statement --sql_file "test/db.sql" --output stu_meta.yml').read()
        s = list(os.walk('.'))
        self.assertIn('stu_meta.yml', s[0][-1])

    def test_from_file1(self):
        print(os.popen('table2yml table_name --connect mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital --table_names "information_sick,cpc_basis,cpc_emergency_info,cpc_treatment_info,cpc_treatment_pci_info,cpc_out_come_info,cpc_coronary_angiographie" --output cpc_case_meta.yml').read())
        s = list(os.walk('.'))
        self.assertIn('cpc_case_meta.yml', s[0][-1])

    def test_from_db(self):
        os.popen('table2yml table_name --table_names "report_info,cpc_field_info" --connect mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital --output report_info.yml').read()
        s = list(os.walk('.'))
        self.assertIn('report_info.yml', s[0][-1])

if __name__ == '__main__':
    unittest.main()
