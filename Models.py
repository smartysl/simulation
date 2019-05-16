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
        self.preEvent=None
    def register(self,node):
        self.nodeGroup.append(node)
    def unregister(self,node):
        self.nodeGroup.pop(self.nodeGroup.index(node))
    def notify(self,event):
        buffer=[]
        for node in self.nodeGroup:
            node.update(event,self.preEvent,buffer,self.time,self.lastTime)#将当前信道时间传入节点中以判断是否发生冲突
        self.time=max(self.time,event.endTime) #记录当前时间
        self.lastTime=max(self.lastTime,self.time) #记录事件中最后的时间
        for e in buffer:
            self.lastTime=max(self.lastTime,e.endTime)
        self.preEvent=event
        return buffer
class Node:
    def __init__(self,id):
        self.id=id
        self.status=DORMANT_STATE
        self.sendBuffer=[]#缓冲已发送的信息以便冲突后回滚
        self.receiveBuffer=[]
        self.protocol=Protocol(self)
        self.logger=Logger()
    def eventConflict(self,event,preEvent):
        return event.startTime>preEvent.startTime
    def update(self,event,preEvent,buffer,time,lastTime):
        # 调用相关协议,返回回调事件并加入buffer中
        # 每个事件都要等确认无冲突后才能log
        # 发送者确认无冲突后清空缓冲，接收者无论是否冲突都会清空缓冲
        # 所有协议调用的前提是有冲突发生
        # 冲突分为事件冲突和信道冲突
        isSafe=True #标记缓冲区中事件安全
        if event.startTime<time: #有冲突发生
            if self.eventConflict(event,preEvent): #事件冲突
                if event.sender==self:
                    new=Event(**event.__dict__)
                    new.endTime=new.endTime-new.startTime+lastTime
                    new.startTime=lastTime #更新时间戳
                    buffer.append(new) #重发
            else: #信道冲突
                isSafe=False
                if event.sender==self:
                    pass #调用协议
                elif event.receiver==self:
                    pass #调用协议
                else:
                    pass #调用协议
        if isSafe:
            while(self.sendBuffer):
                if self.sendBuffer[0].startTime==preEvent.startTime: #通过时间戳判断是否是堆积的消息
                    self.logger.log(SendMessage(self.sendBuffer.pop(0)))
                else:
                    newEvent=self.sendBuffer.pop(0)
                    newEvent.endTime = newEvent.endTime - newEvent.startTime + time
                    newEvent.startTime = time
                    buffer.append(newEvent) #如果缓冲区有未发送的event,需要在冲突解决后打上新的时间戳,并推入buffer中
            while(self.receiveBuffer):
                self.logger.log(ReceiveMessage(self.receiveBuffer.pop(0)))
        else:
            self.receiveBuffer=[] #清空接受缓冲区
        # 这里设计的不好
        if not (event.startTime<time and self.eventConflict(event,preEvent)):
            if event.sender == self:
                self.sendBuffer.append(event) #只要不是事件冲突都将缓冲该发送事件
            elif event.receiver==self:
                self.receiveBuffer.append(event)
    def talk(self,parameter,buffer):
        buffer.append(Event(**parameter))


