from Protocol import Protocol
from logger import Logger,SendMessage,ReceiveMessage
APPLY_EVENT=0
MESSAGE_EVENT=1
NOTICE_EVENT=2
DORMANT_STATE=0
LINSTENING_STATE=1
class Event:
    def __init__(self,code,sender,receiver,body,startTime,endTime):
        self.startTime=startTime
        self.endTime=endTime
        self.code=code #分为告知和发送消息
        self.sender=sender
        self.receiver=receiver
        self.body=body
class Channel:
    #承担观察者角色
    def __init__(self,start,nodeGroup):
        self.time=start
        self.lastTime=start
        self.nodeGroup=nodeGroup
    def register(self,node):
        self.nodeGroup.append(node)
    def unregister(self,node):
        self.nodeGroup.pop(self.nodeGroup.index(node))
    def notify(self,events):
        buffer=[]
        for node in self.nodeGroup:
            node.update(events,buffer,self.time,self.lastTime)#将当前信道时间传入节点中以判断是否发生冲突
        for event in events:  #记录当前时间
            self.time=max(self.time,event.endTime)
        for newEvent in buffer:
            self.lastTime=max(self.lastTime,newEvent.endTime)
        return buffer
class Node:
    def __init__(self,id):
        self.id=id
        self.status=LINSTENING_STATE
        self.sendBuffer=[]#缓冲已发送的信息以便冲突后回滚
        self.protocol=Protocol()
        self.logger=Logger()
        self.time=0
    def update(self,events,buffer,time,lastTime):
        # 调用相关协议,返回回调事件并加入buffer中
        # 每个事件都要等确认无冲突后才能log
        # 所有协议调用的前提是有冲突发生
        self.buffer=buffer
        self.lastTime=time
        for event in events:  #记录当前时间
            self.lastTime=max(self.lastTime,event.endTime)
        if events[0].startTime < time:  # 有事件冲突发生
            for event in events:
                if event.sender == self:
                    self.resend(event,buffer,lastTime)
            return buffer
        if len(events)>1: #发生信道冲突
            self.protocol.handle(self,events)
        else:
            event=events[0]
            if event.code==NOTICE_EVENT:
                self.protocol.retry(self)
            else:
                while(self.sendBuffer):
                    newEvent=self.sendBuffer.pop(0)
                    self.resend(newEvent,buffer,lastTime)
            if event.sender==self:
                self.logger.log(SendMessage(event))
            elif event.receiver==self:
                self.logger.log(ReceiveMessage(event))
        return buffer
    def resend(self,event,buffer,lastTime):
        new = Event(**event.__dict__)
        new.endTime = new.endTime - new.startTime + lastTime
        new.startTime = lastTime  # 更新时间戳
        buffer.append(new)  # 重发
    def send(self,params,buffer):
        buffer.append(Event(**params))
    def load(self,event):
        self.sendBuffer.append(event)


