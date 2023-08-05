import socket
import re
from queue import Queue

class queue:
    __host=None
    __port=None
    __token=None
    __connection=None
    __taskInfo=None
    __unfinishData=None
    __waitSendQueue=None
    __waitConsumerQueue=None
    __uniqueId=None
    __unfinishedBuffer=""
    def __init__(self,taskInfo):
        self.__taskInfo=taskInfo
        self.__waitSendQueue=Queue()#等待发送的数据
        self.__waitConsumerQueue=Queue()#等待消费的队列
        self.__host=self.__taskInfo['host']
        self.__port=self.__taskInfo['port']
        self.__token=self.__taskInfo['token']
        self.__uniqueId=self.__taskInfo['uniqueTaskId']
        self.__connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__connection.connect((self.__host,self.__port))
        pass
    ## 非阻塞的返回数据 若没有数据直接返回
    def send(self,msg):
        msg['uniqueTaskId']=self.__uniqueId
        self.__connection.send(self.packetData(msg).encode())

    def unblockingRecv(self):
        self.__connection.setblocking(False)
        return self.__connection.recv(1024)
    ## 阻塞的返回数据
    def blockRecv(self):
        while True:
            buffer=self.__connection.recv(1024).decode()
            buffer=self.__unfinishedBuffer+buffer
            bufferInfo=self.unpackData(buffer)
            if bufferInfo['isFinished']==True:
                self.__unfinishedBuffer=bufferInfo['resBuffer']
                return bufferInfo['buffer']
            else:
                self.__unfinishedBuffer=self.__unfinishedBuffer+buffer
    def packetData(self,data):
        dataByte=bytes(data,encoding='utf-8')
        header="--#&content-length:{}&chunk:{}&index:{}&#--".format(len(dataByte),0,1)
        return header+data
    def unpackData(self,data):
        reg=re.compile("--#&content-length:(.*?)&chunk:(.*?)&index:(.*?)&#--")
        matchs=reg.findall(data)
        if(len(matchs)==0):
            return None
        if matchs is not None:
            start = reg.match(data).group()
            contentLength=matchs[0]
            contentIndex=int(start)+int(contentLength)
            if contentIndex>len(data):
                contentIndex=len(data)
            content=data[start:contentIndex]
            return {
                "buffer":content,
                "resBuffer":data[contentIndex:len(data)],
                "isFinished":len(content)>=contentLength,
                "unFinishBufferLength":contentLength-len(content),
            }
        return None

