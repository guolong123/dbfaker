# coding=utf-8
import pymysql
from dbutils.pooled_db import PooledDB
from dbutils.persistent_db import PersistentDB

# 数据库配置信息
db_info = {}


class DBHelper:
    """数据库连接助手"""
    __POOL = None

    def __init__(self, drivername='pymysql'):
        self.conn = self.__get_conn(drivername)
        self.cur = self.conn.cursor()

    @staticmethod
    def __get_conn(drivername):
        """获取连接"""
        global __POOL
        if drivername == 'sqlite':
            engine = PersistentDB
            db = db_info['db']
            creator = db_info['creator']
            db_info.clear()
            db_info['database'] = db
            db_info['creator'] = creator
        else:
            engine = PooledDB

        if DBHelper.__POOL is None:
            __POOL = engine(**db_info)
        return __POOL.connection()

    @staticmethod
    def db_setting(db, creator=pymysql, user='root', passwd='123456', host='localhost', port=3306):
        """设置数据库配置信息"""
        db_info.update({
            'db': db,
            'creator': creator,
            'user': user,
            'passwd': passwd,
            'host': host,
            'port': port,
            'autocommit': 1
        })

    def execute(self, sql):
        """执行SQL语句"""
        effect_num = self.cur.execute(sql)
        return effect_num

    def commit(self):
        """提交操作"""
        self.conn.commit()

    def rollback(self):
        """回滚操作"""
        self.conn.rollback()

    def dispose(self):
        """释放连接"""
        self.cur.close()
        self.conn.close()
