import pymysql

from utils.handle_data.configParse import ConfigParse

configParse = ConfigParse()


class MysqlConnect:
    def __init__(self):
        self.conf = {
            "host": configParse.get_value("Mysql", "host"),
            "port": int(configParse.get_value("Mysql", "port")),
            "user": configParse.get_value("Mysql", "user"),
            "password": configParse.get_value("Mysql", "password"),
            "database": configParse.get_value("Mysql", "database"),
        }
        try:
            self.conn = pymysql.connect(**self.conf)
            # 获取操作游标
            self.cursor = self.conn.cursor()
            print(f'成功连接数据库{self.conf['database']}')
        except Exception as e:
            print(f'连接失败原因{e} ')

    def query(self, sql, fetchall=False):
        """
        :param sql:  查询语句
        :param fetchall: 是否查询全部 默认查询单条
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            if fetchall:
                res = self.cursor.fetchall()
            else:
                res = self.cursor.fetchone()
            return res
        except Exception as e:
            print('查询数据库内存出现异常', e)


if __name__ == '__main__':
    db = MysqlConnect()
    sql = "select * from address"
    print(db.query(sql))
