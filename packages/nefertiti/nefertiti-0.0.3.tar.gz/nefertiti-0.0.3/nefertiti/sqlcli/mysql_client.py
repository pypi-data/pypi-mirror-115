import MySQLdb

from nefertiti.sqlcli.base_sql_client import BaseSqlClient


class MysqlClient(BaseSqlClient):

    """
    原生sql语句中的param通配符使用 %s, 不加引号
    """

    def __init__(self, database, user, password, host, port=3306, charset='utf8'):
        """MySQL Database"""
        self.conn = MySQLdb.connect(host=host, user=user, password=password, database=database, port=port, charset=charset)
