from common.setting import get_yaml
import pymysql
import sys

sys.modules["MySQLDB"] = sys.modules["_mysql"] = sys.modules["pymysql"]
setting = get_yaml('setting.yml')
_database = setting.get('database')
database_type = _database.get("type")
database_connect = _database.get("connect")