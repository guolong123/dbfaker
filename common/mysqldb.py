import pymysql
import datetime
import time
import sys
from common.drivers import load_sqlalchemy, load_conn
sys.modules["MySQLDB"] = sys.modules["_mysql"] = sys.modules["pymysql"]


class Database:
    def __init__(self, db_session):
        self.db = load_conn(db_session).connection.connection

    def select(self, table, where=None):
        """
        执行查询操作
        :param table:
        :param where:
        :return:
        """
        cur = self.db.cursor()
        if not where:
            sql = "select * from {}".format(table)
        else:
            sql = "select * from {table} ".format(table=table) + "where " + where
        cur.execute(sql)
        result = cur.fetchall()
        results = []
        col = [x[0] for x in cur.description]
        for i in result:
            data = dict(zip(col, i))
            results.append(data)
        return results

    def select2(self, table, where=None):
        """
        执行查询操作
        :param table:
        :param where:
        :return:
        """
        cur = self.db.cursor()
        if not where:
            sql = "select * from {}".format(table)
        else:
            ls = [(k, where[k]) for k in where if where[k]]
            sql = "select * from {table} where ".format(table) + ' and '.join([i[0] + "=%r" % i[1] for i in ls])
        cur.execute(sql)
        result = cur.fetchall()
        results = []
        col = [x[0] for x in cur.description]
        for i in result:
            data = dict(zip(col, i))
            results.append(data)
        return results

    def select3(self, sql):
        """
        执行查询操作
        :param table:
        :param where:
        :return:
        """
        cur = self.db.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        results = []
        col = [x[0] for x in cur.description]
        for i in result:
            data = dict(zip(col, i))
            results.append(data)
        return results

    def query(self, sql, raise_=True):
        """
        执行增删改操作
        :param sql:
        :return:
        """
        # print(sql)
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            if raise_:
                raise

    def insert(self, table, fields):
        """
        执行新增操作
        :param table:
        :param fields:
        :return:
        """
        keys = ', '.join(list(fields.keys()))
        values = tuple(fields.values())
        sql = "INSERT INTO {table}({keys}) value {values}".format(table=table, keys=keys, values=values)
        self.query(sql)

    def query_table(self, table_name):
        sql = f'show create table {table_name};'
        cur = self.db.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result[0][1]

    def insert2(self, table, fields):
        """
        执行新增操作
        :param table:
        :param fields:
        :return:
        """
        ls = [(k, fields[k]) for k in fields if fields[k]]
        sql = "insert into {table} set ".format(table) + ', '.join([i[0] + "=%r" % i[1] for i in ls])
        self.query(sql)

    def close(self):
        self.db.close()


if __name__ == "__main__":
    db = Database(db_session='mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital')
    # db.query('select * from report_info')
    s = db.query_table('report_info')

    print(s)
    s = db.select3('select * from report_info limit 1;')
    print(s)