import requests
import json
from whTool.wh_Log import Log
import whTool.wh_Global
import traceback

class WebService(object):
    def __init__(self):
        self.se = requests.session()

    # GET方法
    def Get(self, url, params=None):
        whTool.wh_Global.logger.info('调用链路|' + str(traceback.extract_stack()))
        try:
            whTool.wh_Global.logger.info('接口调用' + '|url:' + str(url) + '|params:' + str(params))
            res = self.se.get(url=url, params=params)
            res_dict = res.json()
            whTool.wh_Global.logger.info('接口返回' + '|res:' + str(res) + '|res_dict:' + str(res_dict))
            return res_dict
        except Exception as e:
            whTool.wh_Global.logger.warning('调用链路|' + str(traceback.extract_stack()))
            whTool.wh_Global.logger.warning('接口调用' + '|url:' + str(url) + '|params:' + str(params))
            whTool.wh_Global.logger.error(e)

    # POST方法
    def Post(self, url, data=None, json=None):
        whTool.wh_Global.logger.info('调用链路|' + str(traceback.extract_stack()))
        try:
            whTool.wh_Global.logger.info('接口调用' + '|url:' + str(url) + '|data:' + str(data) + '|json:' + str(json))
            res = self.se.post(url=url, data=data, json=json)
            res_dict = res.json()
            whTool.wh_Global.logger.info('接口返回' + '|res:' + str(res) + '|res_dict:' + str(res_dict))
            return res_dict
        except Exception as e:
            whTool.wh_Global.logger.warning('调用链路|' + str(traceback.extract_stack()))
            whTool.wh_Global.logger.warning('接口调用' + '|url:' + str(url) + '|data:' + str(data) + '|json:' + str(json))
            whTool.wh_Global.logger.error(e)







if __name__=='__main__':
    a = WebService()
    data = {"filter":{"name":"","level":"","nowduty":"","seePeriod":["",""],"endPeriod":["",""]},"page":{"pageNumber":1,"pageSize":"10"},"ticket":"d2VuaGFvYw=="}
    res = a.Post(url='http://localhost:8000/alert/getAlertList', json=data)
    print(res)