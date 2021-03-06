from Models import Channel
class Controller:
    #推进事件发展
    def __init__(self,events,channel):
        self.channel=channel
        self.maxDelay=self.channel.maxDelay
        self.queue=[] #缓冲队列
        for event in events:
            self.queue.append(event)#将初始时事件推入
    def run(self):
        while(self.queue):
            events=[self.queue.pop(0)]
            while(self.queue and self.queue[0].startTime<=events[0].startTime+self.maxDelay): #最大时延时间段内的事件全部取出
                events.append(self.queue.pop(0))
            newEvents=[]
            newEvents+=self.channel.notify(events)
            for new in newEvents:
                i=0
                while(i<len(self.queue) and new.startTime>self.queue[i].startTime):
                    i+=1
                self.queue.insert(i,new) #将新事件按照时间顺序插入队列

