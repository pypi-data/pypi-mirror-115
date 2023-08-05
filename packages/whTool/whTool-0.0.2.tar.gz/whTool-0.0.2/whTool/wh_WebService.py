import requests
import json


class WebService(object):
    def __init__(self):
        self.se = requests.session()

    # GET方法
    def Get(self, url, params=None):
        res = self.se.get(url=url, params=params)
        res = res.json()
        return res

    # POST方法
    def Post(self, url, data=None, json=None):
        res = self.se.post(url=url, data=data, json=json)
        res = res.json()
        return res










if __name__=='__main__':
    a = WebService()
    data = {"filter":{"name":"","level":"","nowduty":"","seePeriod":["",""],"endPeriod":["",""]},"page":{"pageNumber":1,"pageSize":"10"},"ticket":"d2VuaGFvYw=="}
    res = a.Post(url='http://localhost:8000/alert/getAlertList', json=data)
    print(res)