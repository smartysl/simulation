from Controller import Controller
from Models import Event,Node,Channel
from logger import Logger
if __name__ == '__main__':
    nodeGroup=[Node(i) for i in range(4)]
    logger=Logger()
    channel=Channel(0,nodeGroup)
    paramtersList=[{
        'startTime':0,
        'endTime':12,
        'code':0,
        'sender':nodeGroup[0],
        'receiver':nodeGroup[1],
        'body':"hello1"
    },{
        'startTime': 1,
        'endTime': 3,
        'code': 0,
        'sender': nodeGroup[1],
        'receiver': nodeGroup[2],
        'body': "hello2"
    },{
        'startTime': 5,
        'endTime': 7,
        'code': 0,
        'sender': nodeGroup[2],
        'receiver': nodeGroup[3],
        'body': "hello3"
    },{
        'startTime': 100,
        'endTime': 120,
        'code': 0,
        'sender': nodeGroup[0],
        'receiver': nodeGroup[1],
        'body': "finish"
    }]
    events=[]
    for paramter in paramtersList:
        events.append(Event(**paramter))
    c=Controller(events,channel)
    c.run()
    logger.output()