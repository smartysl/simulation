from Protocol import Protocol
from logger import Logger,SendMessage,ReceiveMessage
from collections import defaultdict
APPLY_EVENT=0
MESSAGE_EVENT=1
NOTICE_EVENT=2
DORMANT_STATE=0
LINSTENING_STATE=1
LIGHT_SPEED=3*(10**8)
class Event:
    def __init__(self,code,sender,receiver,body,startTime,endTime,resend=False):
        self.startTime=startTime
        self.endTime=endTime
        self.code=code #分为告知和发送消息
        self.sender=sender
        self.receiver=receiver
        self.body=body
        self.resend=resend
class Channel:
    #承担观察者角色
    def __init__(self,start):
        self.time=start
        self.reimbursedTime=0
        self.newConflixNodes=[]
        self.nodeGroup=None
        self.delayMap=defaultdict()
        self.maxDelay=0
    def addGroup(self,group):
        self.nodeGroup=group
        self.buildDelayMap()
    def buildDelayMap(self):
        for i in range(len(self.nodeGroup)):
            for j in range(len(self.nodeGroup)):
                (x1,y1),(x2,y2)=self.nodeGroup[i].location,self.nodeGroup[j].location
                self.delayMap[(self.nodeGroup[i],self.nodeGroup[j])]=((x1-x2)**2+(y1-y2)**2)**0.5/LIGHT_SPEED
                self.delayMap[(self.nodeGroup[j],self.nodeGroup[i])]=((x1-x2)**2+(y1-y2)**2)**0.5/LIGHT_SPEED
        self.maxDelay=max(self.delayMap.values())
    def register(self,node):
        self.nodeGroup.append(node)
    def unregister(self,node):
        self.nodeGroup.pop(self.nodeGroup.index(node))
    def flushProtocol(self):
        find = False
        for node in self.nodeGroup:
            if node.conflix:
                find = True
        if not find:
            self.nodeGroup[0].protocol.flush()
    def notify(self,events):
        buffer=[]
        self.realHappen=True
        for node in self.nodeGroup:
            node.update(events,buffer)#将当前信道时间传入节点中以判断是否发生冲突
        if not self.realHappen:
            return buffer
        for node in self.newConflixNodes:
            node.conflix=True
        self.newConflixNodes=[] # 延时更新节点状态
        for event in events:  #记录当前时间
            self.time=max(self.time,event.endTime)
        self.flushProtocol()
        if self.reimbursedTime!=0:
            if self.reimbursedTime > 0:  # 补偿时延对buffer中时间的影响
                for e in buffer:
                    e.startTime += self.reimbursedTime
                    e.endTime += self.reimbursedTime
            self.time+=self.reimbursedTime
            self.reimbursedTime=0
        return buffer
class Node:
    def __init__(self,id,x,y,channel):
        self.id=id
        self.status=LINSTENING_STATE
        self.sendBuffer=[]#缓冲已发送的信息以便冲突后回滚
        self.protocol=Protocol()
        self.logger=Logger()
        self.time=0
        self.location=(x,y)
        self.conflix=False  # 记录当前节点是否在冲突
        self.channel=channel # 为了直接更改信道时间
    def update(self,events,buffer):
        # 调用相关协议,返回回调事件并加入buffer中
        # 每个事件都要等确认无冲突后才能log
        # 所有协议调用的前提是有冲突发生
        # 在这里的所有新增事件均不考虑时延
        self.buffer=buffer #新生成的事件放在这里
        if events[0].startTime<self.channel.time:  # 有事件冲突发生，将所有事件向后推，但是保持相对时间不变
            for event in events:
                self.channel.realHappen=False
                sub=event.startTime-events[0].startTime
                if event.sender == self:
                    self.resend(event,buffer,self.channel.time+sub)
            return
        if self.applyForEvent(events): #只要当前事件中有未申请的信息，后续一律不处理
            self.channel.realHappen=False
            return
        conflixEvents,otherEvents = self.sepEvent(events)
        if otherEvents:
            return # 如果有插队的事件后续不做处理
        if len(conflixEvents)>1: #冲突事件多于一个才调用协议
            self.channel.reimbursedTime=self.channel.maxDelay
            self.protocol.handle(self,events) #这里将自身传入协议中
        else:
            event=conflixEvents[0] #这里只有一个真正的冲突/事件
            if event.code==NOTICE_EVENT:
                if self.id==0:
                    self.channel.reimbursedTime=(event.sender.id%10)*self.channel.maxDelay #需要延迟更新时间
                if self.conflix: #冲突中的节点尝试重发
                    for newEvent in self.sendBuffer[::-1]:
                        if newEvent.code==APPLY_EVENT:
                            self.sendBuffer.remove(newEvent)
                            self.protocol.retry(self,newEvent)
                            break
            else:
                self.channel.reimbursedTime = self.channel.maxDelay
                if event.code==APPLY_EVENT: # 此时处理apply事件
                    if self==event.sender:
                        for newEvent in self.sendBuffer:
                            if newEvent.code == MESSAGE_EVENT:
                                self.sendBuffer.remove(newEvent)
                                self.resend(newEvent, buffer,event.endTime - event.startTime + self.channel.time)  # 确保没有冲突后由冲突过的节点将带有真实内容的信息发出
                                break
                else:
                    if self.id==0:
                        self.protocol.updateSearchState('backward') # 这里由第一个节点先更新折半区间
                    if self.conflix:
                        if self==event.sender:
                            self.conflix = False # 该节点不再参与竞争
                        else: # 有一个节点胜出后，其他冲突中的节点要将sendBuffer中的apply重新发出继续竞争
                            for newEvent in self.sendBuffer:
                                if newEvent.code==APPLY_EVENT:
                                    self.sendBuffer.remove(newEvent)
                                    newEvent.endTime=newEvent.endTime+event.endTime-event.startTime
                                    newEvent.startTime=newEvent.startTime+event.endTime-event.startTime
                                    self.protocol.retry(self,newEvent)
                                    break
            if event.code==MESSAGE_EVENT and event.resend==False: # 没有经过重发的消息是非法的
                return
            if event.sender==self:
                self.logger.log(SendMessage(event))
            elif event.receiver==self:
                logEvent=Event(**event.__dict__)
                logEvent.endTime+=self.channel.delayMap[(event.sender,event.receiver)] #记录时要加上时延
                self.logger.log(ReceiveMessage(logEvent))
        return
    def applyForEvent(self,events):
        find = False
        memory=[]
        for event in events:
            if event.code == MESSAGE_EVENT and event.resend == False:
                find = True
                if self == event.sender:
                    self.apply(event)
            else:
                memory.append(event)
        if find:
            for event in memory:
                if self==event.sender:
                    self.resend(event,self.buffer,event.startTime) # 其余时间需要原封不动放回去
        return find
    def resend(self,event,buffer,lastTime):
        new = Event(**event.__dict__)
        new.endTime = new.endTime - new.startTime + lastTime
        new.startTime = lastTime  # 更新时间戳
        buffer.append(new)  # 重发
    def sepEvent(self,events): #对同一段时间进入的事件进行区分，其他事件需要重发
        conflixEvents=[]
        otherEvents=[]
        for event in events:
            if event.sender.conflix or event.code==NOTICE_EVENT:
                conflixEvents.append(event)
            else:
                otherEvents.append(event)
        if not conflixEvents:
            conflixEvents,otherEvents=otherEvents,conflixEvents # 此次事件全部为初次冲突
        maxEndTime = 0
        for conflixEvent in conflixEvents:
            maxEndTime = max(maxEndTime, conflixEvent.endTime)
        for otherEvent in otherEvents:
            if self == otherEvent.sender:
                sub = otherEvent.startTime - otherEvents[0].startTime
                self.resend(otherEvent,self.buffer, maxEndTime + sub)  # 取冲突事件中最大结束时间加上偏移量作为其他事件的时间戳重发
        if otherEvents:
            self.channel.realHappen = False
            for conflixEvent in conflixEvents:
                if self == conflixEvent.sender:
                    self.resend(conflixEvent,self.buffer, conflixEvent.startTime)  # 需要将冲突事件传递回去
        return conflixEvents,otherEvents
    def send(self,params,buffer):
        buffer.append(Event(**params))
    def load(self,event):
        self.sendBuffer.append(event)
    def apply(self,event): #为具有实际信息的事件发送申请事件
        newMesEvent=Event(**event.__dict__)
        newMesEvent.resend=True
        newEvent=Event(**event.__dict__)
        newEvent.code=APPLY_EVENT
        newEvent.endTime=event.startTime+0.1
        newEvent.body="APPLY"
        newEvent.receiver=None
        self.buffer.append(newEvent)
        self.sendBuffer.append(newMesEvent) #需要把具有实际消息的事件在发送节点中存起来


