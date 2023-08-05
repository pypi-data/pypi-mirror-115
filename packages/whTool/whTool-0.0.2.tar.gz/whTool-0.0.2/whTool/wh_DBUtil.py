import pymysql


class DBUtil(object):
    def __init__(self, host, db, user, password):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.connect = pymysql.connect(host=self.host, db=self.db, user=self.user, password=self.password, charset="gbk",cursorclass=pymysql.cursors.DictCursor)

    # 测试连接是够有效，无效则重连
    def testConnect(self):
        try:
            self.connect.ping()
        except:
            self.connect = pymysql.connect(host=self.host, db=self.db, user=self.user, password=self.password, charset="gbk",cursorclass=pymysql.cursors.DictCursor)

    # 执行查询sql，成功返回结果，失败返回False
    def Select(self, sql, params=None):
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            cursor.execute(sql, params)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as e:
            return False

    # 执行插入sql，成功返回最后一行的主键，失败返回False
    def Insert(self, sql, param=None):
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            cursor.execute(sql, param)
            self.connect.commit()
            lastRowId = int(cursor.lastrowid)
            return lastRowId
        except Exception as e:
            self.connect.rollback()
            return False

    # 执行删除sql，成功返回True，失败返回False
    def Delete(self, sql, param=None):
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            cursor.execute(sql, param)
            self.connect.commit()
            return True
        except Exception as e:
            self.connect.rollback()
            return False

    # 执行更新sql，成功返回True，失败返回False
    def Update(self, sql, param=None):
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            cursor.execute(sql, param)
            self.connect.commit()
            return True
        except Exception as e:
            self.connect.rollback()
            return False



if __name__=='__main__':
    a = DBUtil(host='localhost', db='esu', user='root', password='123456')
    sql = '''select * from alert_msg'''
    res = a.Select(sql)
    print(res)