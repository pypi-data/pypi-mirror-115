from . import *
import requests
import json
import hashlib
import time

class Request:
    def __init__(self, host, AK, SK, debug=False):
        # self.__TOKEN_URL = 'http://label-export.testin.cn/develope/passport/get-token'
        # self.__TASK_URL = 'http://label-export.testin.cn/develope/task/get-label-data'
        # self.__TOKEN_AK = 'ae1bdbc2d15e4fb4779558f75de21c95'
        # self.__TOKEN_SK = '29de907568f60c9a452f24ef1e0a03b0'

        self.__TOKEN_URL = f'{host}develope/passport/get-token'
        self.__TASK_URL = f'{host}develope/task/get-label-data'
        self.__TOKEN_AK = AK
        self.__TOKEN_SK = SK
        self.__DEBUG = debug


    def __getToken(self):
        data = {
            'access_key': self.__TOKEN_AK,
            'secret_key': self.__TOKEN_SK
        }
        response = requests.post(self.__TOKEN_URL, json=data)
        res = response.json()
        return res['data']['access_token']

    def __getTaskInfo(self, key, has_unable, statuss):
        page = 1
        taskList = []
        res = {}
        status = statuss[0]
        token = self.__getToken()

        hasUnable = 0
        if has_unable: hasUnable = 1

        while status in statuss:
            times = str(int(time.time()))
            data = {
                "task_key": key,
                "page": page,
                "page_num": 20,
                "has_unable": hasUnable,
            }
            _sign = '&'.join([f'{k}={v}' for k, v in sorted(data.items(), key=lambda d: d[0])])
            s = token + _sign + times
            sign = hashlib.md5(s.encode('utf8')).hexdigest()
            data.update({"sign": sign, "access_token": token, "time": times, "status": status})
            page += 1
            r = requests.post(self.__TASK_URL, json=data, headers={'Content-Type': 'application/json'})
            res = r.json()
            if self.__DEBUG and res['data'] != {}:
                print(f"[DOWNLOAD_LABEL_DATA] download labeled data from server, taskName:{res['data']['taskName']}, status:{status}, taskTotal:{res['data']['total']}, current Page:{res['data']['page']}, per page items:{res['data']['pageNum']}")
            if not res['data'] or not res['data']['taskList']:
                log_info = r.json()
                log_info['key'] = key
                log_info['status'] = status
                status += 1
                page = 1
                continue
            taskList += res['data']['taskList']
        if res: res['data']['taskList'] = taskList
        return res

    def getTaskData(self, key, hasUnable=False, status=[STATUS_PASS, STATUS_CHECK_WAIT, STATUS_INSPECTOR_WAIT]):
        markDatas = self.__getTaskInfo(key=key, has_unable=hasUnable, statuss=status)
        return markDatas

    def getAllTaskInfo(self, keys, json_path, has_unable=0, status=2, statuss=[2, 3, 4]):
        task_all_info = {key: self.__getTaskInfo(key, status, statuss, has_unable) for key in keys if key}
        with open(json_path, 'w') as f:
            f.write(json.dumps(task_all_info))
