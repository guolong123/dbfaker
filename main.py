from utils.gendata import GenData


def loop(loop_cnt=1, meta_file=None, insert=False):
    n = 0
    if not meta_file:
        meta_file = 'data/ecg_report_meta.yml'
    while n < loop_cnt:
        handler = GenData(meta_file)
        mock_data = handler.pre()
        for d in mock_data:
            sqls = handler.dict2sql(d)
            for sql in sqls:
                handler.insert2db(sql, insert)
        print('\n\n')
        n += 1


if __name__ == '__main__':
    loop(1, meta_file='data/information_sick_meta.yml')
    loop(1, meta_file='data/cpc_case_meta.yml')
    loop(1)
