# encoding: utf-8
import importlib
import json

import awesomeTaskPy
from awesomeTaskPy.context.context import context
import time
import sys
import traceback


class baseTask():
    __taskInfo = None
    __loger = None
    __modulePath = None
    __startAt = None
    __startAtTime = None

    def __now(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __nowInt(self):
        return int(time.time())

    def __init__(self, taskInfo, modulePath):
        self.__taskInfo = taskInfo
        self.__modulePath = modulePath
        self.__startAt = self.__now()
        self.__startAtTime = self.__nowInt()
        try:
            res = self.__run()
            output = {
                "startAt": self.__startAt,
                "endAt": self.__now(),
                "runTime": self.__nowInt() - self.__startAtTime,
                "result": res,
                "error":None
            }
            # 回调返回值并且情况缓冲的日志
            awesomeTaskPy.context.context.getContext().getLoger().writeRes(output).flushTmpLog()
        except:
            traceback.print_exc()  # 打印异常信息

            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))  # 将异常信息转为字符串
            output = {
                "startAt": self.__startAt,
                "endAt": self.__now(),
                "runTime": self.__nowInt() - self.__startAtTime,
                "result": None,
                "error":str(error)
            }
            # 回调返回值并且情况缓冲的日志
            awesomeTaskPy.context.context.getContext().getLoger().writeRes(output).flushTmpLog()
    def log(self, message):
        return  awesomeTaskPy.context.context.getContext().getLoger().write(message)

    # 具体的代码实现逻辑
    def __run(self):
        if "input" in self.__taskInfo.keys():
            input = self.__taskInfo['input']
        else:
            input=[]
        res = importlib.import_module(self.__modulePath).run(*input)
        return res
    ##远程执行函数 获取调用的结果
    @staticmethod
    def apply(fun,*args):
        contextObj=awesomeTaskPy.context.context.getContext()
        RPC={
            "event":"ON_TASK_NODE_REMOTE_FOKE",
            "module":fun.__module__,
            "fun":fun.__name__,
            "class":fun.__class__,
            "argv":args,
            "project":contextObj.getTaskInfo()["project_name"]
        }
        RPCmsg=json.dumps(RPC)
        contextObj.getQueue().send(RPCmsg)
        return contextObj.getQueue().blockRecv()

def outputAndFork(output):
    return awesomeTaskPy.context.context.getContext().getLoger().writeOutputAndFork(output)
