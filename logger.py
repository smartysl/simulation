class Message:
    def __init__(self,event):
        self.event=event
class SendMessage(Message):
    def __init__(self,event):
        super().__init__(event)
    def __str__(self):
        return str(self.event.startTime)+":节点"+str(self.event.sender.id)+"发送了"+str(self.event.body)+"向"+str(self.event.receiver.id)
class ReceiveMessage(Message):
    def __init__(self,event):
        super().__init__(event)
    def __str__(self):
        return str(self.event.endTime) + ":节点" + str(self.event.receiver.id) + "接受了" + str(self.event.body) + "从" + str(
            self.event.sender.id)
class Logger:
    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger,cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.messageList=[]
    def log(self,message):
        self.messageList.append(message)
    def output(self):
        for message in self.messageList:
            print(str(message))