# -*- encoding: utf-8 -*-
import pymysql
from dbfaker.common.drivers import load_sqlalchemy, load_conn
from dbfaker.common.db_helper import DBHelper
from sqlalchemy.engine import url

pymysql.install_as_MySQLdb()


class Database:
    db = None

    def __init__(self, db_session=None):
        self.__init_db(db_session)

    @classmethod
    def __init_db(cls, db_session):
        if not cls.db and db_session:
            cls.drivername, db_config = cls.__analyse_db_session(db_session)
            DBHelper.db_setting(**db_config)
            cls.db = DBHelper(cls.drivername)

    @staticmethod
    def __analyse_db_session(db_session):
        url_config = url.make_url(db_session)
        entrypoint = url_config._get_entrypoint()
        dialect_cls = entrypoint.get_dialect_cls(url_config)
        dbapi = dialect_cls.dbapi()

        db_config = {
            'creator': dbapi,
            'host': url_config.host,
            'user': url_config.username,
            'passwd': url_config.password,
            'db': url_config.database,
            'port': url_config.port
        }

        return url_config.drivername, db_config

    def select(self, table, where=None):
        """
        执行查询操作
        :param table:
        :param where:
        :return:
        """
        cur = self.db.cur
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
        cur = self.db.cur
        if not where:
            sql = "select * from {}".format(table)
        else:
            ls = [(k, where[k]) for k in where if where[k]]
            sql = "select * from {} where ".format(table) + ' and '.join([i[0] + "=%r" % i[1] for i in ls])
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
        cur = self.db.cur
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
        cur = self.db.cur
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print(str(e) + "\n" + sql)
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
        if self.drivername == 'sqlite':
            sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name = '{}'".format(table_name)
            self.db.cur.execute(sql)
            result = self.db.cur.fetchall()
            return result[0][0]
        else:
            sql = 'show create table {table_name};'.format(table_name=table_name)
            self.db.cur.execute(sql)
            result = self.db.cur.fetchall()
            return result[0][1]

    def insert2(self, table, fields):
        """
        执行新增操作
        :param table:
        :param fields:
        :return:
        """
        ls = [(k, fields[k]) for k in fields if fields[k]]
        sql = "insert into {} set ".format(table) + ', '.join([i[0] + "=%r" % i[1] for i in ls])
        self.query(sql)

    def close(self):
        self.db.dispose()


if __name__ == '__main__':
    db = Database(db_session='mysql+mysqldb://root:mysql123@cpcs.homelabs.in/center')
    r = db.select3('select id, username from t_sys_user where id=1')
    print(r)
    r = db.select3('select id, username from t_sys_user where id=1')
    print(r)
