import Models
class Protocol:
    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'instance'):
            cls.instance=super(Protocol,cls).__new__(cls)
        return cls.instance
    def __init__(self):#这里应当记录协议状态
        self.searchStart=0
        self.searchEnd=4
        self.searchStack=[0,4]
        self.conflix=False
    def handle(self,node,events):
        self.conflix=True
        self.notify(node,events)
        for event in events:
            if event.sender==node:
                node.load(event) #把未发送的事件存储起来
                node.channel.newConflixNodes.append(node) #这里需要延迟更新冲突状态
    def retry(self,node,event):
        if node.id>=self.searchStart and node.id<self.searchEnd: #符合折半条件的节点重新发送
            node.resend(event,node.buffer,node.channel.time+0.1) #加上通知事件的持续时间
        else:
            node.load(event) #不符合折半条件的需要装回去
    def notify(self,node,events):
        if not node.status==Models.LINSTENING_STATE:
            return
        for event in events:
            if node==event.sender:
                return
        for event in node.buffer:
            if event.code==Models.NOTICE_EVENT: #检测到之前有节点通知过了就不必通知
                return
        self.updateSearchState('forward') #需要通知将折半区间前推
        lastEventTime=events[0].endTime
        lastEvent=events[0]
        for event in events:
            if event.endTime>lastEvent.endTime:
                lastEventTime=event.endTime
                lastEvent=event
        params={
            'startTime':lastEventTime, #这里也不计算时延
            'endTime':lastEventTime+0.1,
            'code':Models.NOTICE_EVENT,
            'sender':node,
            'receiver':None,
            'body':'notify'
        }
        node.send(params,node.buffer)
    def updateSearchState(self,mark):
        if mark=='forward':
            middle=(self.searchEnd-self.searchStart)//2
            self.searchStack.append(middle)
            self.searchEnd=middle
        else:
            self.searchStart=self.searchStack.pop()
            self.searchEnd=self.searchStack[-1]
    def flush(self):
        self.__init__() # 更新折半状态