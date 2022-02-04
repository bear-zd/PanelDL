import pymysql
from private import DATABASE_CONFIG
from exception import error


class mysqlConnect():
    def __init__(self, connectConfig=DATABASE_CONFIG):
        self.config = connectConfig
        self.cursorType = pymysql.cursors.DictCursor
        self.__conn()

    def __conn(self):
        self.connect = pymysql.connect(**self.config)
        self.cursor = self.connect.cursor()
        print('connected')

    def __reConn(self):
        try:  # 监测是否断连
            self.connect.ping()
        except:
            self.__conn()

    def query(self, sql: str = ''):
        """
        :param sql: sql语句
        :return: 查询返回数量
        """
        self.__reConn()
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            self.cursor.close()
            return True, result
        except:
            print("Quary error")
            return False, None

    def select(self, sql: str):
        self.__reConn()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            return True, result
        except:
            print('Select Error')
            return False, None

    def selectLimit(self, sql: str, offset: int = 0, length: int = 20):
        sql = '%s limit %d , %d ;' % (sql, offset, length)
        self.select(sql)

    def close(self):
        self.__reConn()
        self.connect.close()


if __name__ == '__main__':
    pass
    '''删除注释来测试这部分的代码
    op = mysqlConnect(DATABASE_CONFIG)
    for i in range(5):
        print(op.query('SHOW TABLES;'))
    '''
