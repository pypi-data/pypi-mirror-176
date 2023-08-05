"""
    MYSQL 连接类

    示例：
        engine = MysqlSQLAlchemyEngine(host='localhost', port=3306, user='root', pwd='1234', db='test')
"""
from quickdb.orm.sqlalchemy.engine import SQLAlchemyEngineBase


class MysqlSQLAlchemyEngine(SQLAlchemyEngineBase):
    def __init__(self, db: str, host: str = '127.0.0.1', port: int = '3306', user: str = 'root', pwd: str = None,
                 **kwargs):
        """

        :param host: ip
        :param port: port
        :param user: 账号
        :param pwd: 密码
        :param db: 对应的数据库
        :param kwargs: 其余 SQLAlchemy 参数
        """
        super().__init__('mysql+pymysql', host, port, user, pwd, db, **kwargs)
