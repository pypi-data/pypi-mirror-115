import pymysql
from whTool.wh_Log import Log
import whTool.wh_Global
import traceback

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
            whTool.wh_Global.logger.warning('DB连接断开，尝试重新链接')
            self.connect = pymysql.connect(host=self.host, db=self.db, user=self.user, password=self.password, charset="gbk",cursorclass=pymysql.cursors.DictCursor)

    # 执行查询sql，成功返回结果，失败返回False
    def Select(self, sql, params=None):
        whTool.wh_Global.logger.info('调用链路|' + str(traceback.extract_stack()))
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            whTool.wh_Global.logger.info('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            cursor.execute(sql, params)
            res = cursor.fetchall()
            whTool.wh_Global.logger.info('执行返回' + '|res:' + str(res))
            cursor.close()
            return res
        except Exception as e:
            whTool.wh_Global.logger.warning('调用链路|' + str(traceback.extract_stack()))
            whTool.wh_Global.logger.warning('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            whTool.wh_Global.logger.error(e)
            return False

    # 执行插入sql，成功返回最后一行的主键，失败返回False
    def Insert(self, sql, params=None):
        whTool.wh_Global.logger.info('调用链路|' + str(traceback.extract_stack()))
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            whTool.wh_Global.logger.info('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            cursor.execute(sql, params)
            self.connect.commit()
            lastRowId = int(cursor.lastrowid)
            whTool.wh_Global.logger.info('执行返回' + '|res:' + str(lastRowId))
            return lastRowId
        except Exception as e:
            self.connect.rollback()
            whTool.wh_Global.logger.warning('调用链路|' + str(traceback.extract_stack()))
            whTool.wh_Global.logger.warning('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            whTool.wh_Global.logger.error(e)
            return False

    # 执行删除sql，成功返回True，失败返回False
    def Delete(self, sql, params=None):
        whTool.wh_Global.logger.info('调用链路|' + str(traceback.extract_stack()))
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            whTool.wh_Global.logger.info('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            cursor.execute(sql, params)
            self.connect.commit()
            whTool.wh_Global.logger.info('执行返回' + '|res:' + str(True))
            return True
        except Exception as e:
            self.connect.rollback()
            whTool.wh_Global.logger.warning('调用链路|' + str(traceback.extract_stack()))
            whTool.wh_Global.logger.warning('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            whTool.wh_Global.logger.error(e)
            return False

    # 执行更新sql，成功返回True，失败返回False
    def Update(self, sql, params=None):
        whTool.wh_Global.logger.info('调用链路|' + str(traceback.extract_stack()))
        try:
            self.testConnect()
            cursor = self.connect.cursor()
            whTool.wh_Global.logger.info('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            cursor.execute(sql, params)
            self.connect.commit()
            whTool.wh_Global.logger.info('执行返回' + '|res:' + str(True))
            return True
        except Exception as e:
            self.connect.rollback()
            whTool.wh_Global.logger.warning('调用链路|' + str(traceback.extract_stack()))
            whTool.wh_Global.logger.warning('sql执行' + '|sql:' + str(sql) + '|params:' + str(params))
            whTool.wh_Global.logger.error(e)
            return False



if __name__=='__main__':
    whTool.wh_Global.logger = Log(level='info').getLogger()
    a = DBUtil(host='localhost', db='esu', user='root', password='123456')
    sql = '''select * from alert_msg where id  50'''
    res = a.Select(sql)
    print(res)