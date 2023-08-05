"""
    MongoConn：一个实例一个连接

    通过 get_collection 返回的是 MongoMethod 实例
"""
from typing import NoReturn
from pymongo import MongoClient
from pymongo.results import UpdateResult
from pymongo.collection import Collection


class MongoMethod(Collection):
    """
    继承 Collection 实现自定义方法
    """

    def __init__(self, database, name: str, **kwargs):
        super().__init__(database, name, **kwargs)

    def upsert_one(self, data: dict, filter_keys: list = None) -> UpdateResult:
        """
        更新或插入单条

        :param data:
        :param filter_keys: 需要根据哪些键去重
        :return:
        """
        filter_data = {}

        for filter_key in filter_keys:
            filter_data.update({filter_key: data[filter_key]})

        return self.update_one(data, {'$set': filter_data}, True)

    def __bool__(self) -> NoReturn:
        pass


class MongoConn:
    def __init__(self, user: str = None, pwd: str = None, host: str = '127.0.0.1', port: int = 27017, **kwargs):
        """

        :param user:
        :param pwd:
        :param host: ip
        :param port: 端口
        """
        self.conn = MongoClient(host=host, port=port, username=user, password=pwd, **kwargs)
        self._conn_map = {}

    def get_collection(self, db: str, col: str) -> MongoMethod:
        """
        获取集合连接

        :param db: 库名
        :param col: 集合名
        :return:
        """
        if db not in self._conn_map:
            self._conn_map[db] = {}

        if col not in self._conn_map[db]:
            self._conn_map[db][col] = MongoMethod(database=self.conn[db], name=col)

        return self._conn_map[db][col]

    def close(self):
        """
        关闭连接

        :return:
        """
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    m = MongoConn(host='192.168.0.143', port=9811)
    c = m.get_collection('patent', 'patent_fee')
    r = c.find_one({'doc_no': '2020111723796'})
    print(r)
