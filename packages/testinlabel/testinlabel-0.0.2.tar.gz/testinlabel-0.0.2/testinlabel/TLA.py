from . import *
from testinlabel.request import Request
import os
import json

class TLA():
    def __init__(self, accessKey, secretKey, host="", debug=False, savePath=""):
        if host == "":
            self.host = "http://label-export.testin.cn/"
        else:
            if "http://" in host or "https://" in host:
                self.host = host.rstrip("/") + "/"
            else:
                self.host = "http://" + host.strip("/") + "/"
        self.__debug = debug
        self.AK = accessKey
        self.SK = secretKey
        self.savePath = savePath
        self.req = Request(host=self.host, AK=self.AK, SK=self.SK, debug=self.__debug)
        self.data = None
        self.taskList = None
        self.taskKey = None
        self.jsonDir = None
        self.jsonPath = None


    def SetKey(self, taskKey):
        '''
        Set the dataset to be processed
        :param datasetId: the id of the dataset
        :return:
        '''
        self.taskKey = taskKey

        if self.__debug:
            print(f"[SET_TASK_KEY] set task key:{taskKey}")

        self.jsonDir = os.path.join(self.savePath, "testinlabel-data", self.taskKey)
        if not os.path.exists(self.jsonDir):
            os.makedirs(self.jsonDir)

        self.jsonPath = os.path.join(self.jsonDir, taskKey + ".json")

        if os.path.exists(self.jsonPath):
            with open(self.jsonPath, "r", encoding="utf-8") as jf:
                self.data = json.load(jf)
                self.taskList = self.data["data"]["taskList"]


    def GetLabelData(self, hasUnable=False, status=[STATUS_PASS], overlay=False):
        """
        get labeled data by task_key, more about task_key, see: http://label.testin.cn/v/pm-task-list
        :param taskKey:
        :param hasUnable:
        :param status:
        :param save:
        :return:
        """
        if self.data != None and overlay == False:
            if self.debug:
                print(f"[GET_LABEL_DATA] label data already download to locah path: {self.jsonPath}, abort this request！if you need re-download anyway, you should set overlay to Ture")
            self.taskList = self.data["data"]["taskList"]
            return self.data

        self.data = self.req.getTaskData(key=self.taskKey, hasUnable=hasUnable, status=status)

        with open(self.jsonPath, "w", encoding="utf-8") as f:
            json.dump(self.data, f)
            if self.__debug:
                print(f"[SAVE_LABEL_DATA] save data to:{self.jsonPath}")

        self.taskList = self.data["data"]["taskList"]
        return self.data

