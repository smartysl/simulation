from Controller import Controller
from Models import Event,Node,Channel
from logger import Logger
import Models
if __name__ == '__main__':
    channel=Channel(0)
    nodeGroup=[
        Node(0,1,2,channel),
        Node(1,3,5,channel),
        Node(2,4,5,channel),
        Node(3,6,7,channel)
    ]
    channel.addGroup(nodeGroup)
    logger=Logger()
    paramtersList=[{
        'startTime':0,
        'endTime':1,
        'code':Models.MESSAGE_EVENT,
        'sender':nodeGroup[0],
        'receiver':nodeGroup[1],
        'body':"hello1"
    },{
        'startTime': 0,
        'endTime': 1,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[1],
        'receiver': nodeGroup[2],
        'body': "hello2"
    },{
        'startTime': 1,
        'endTime': 2,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[2],
        'receiver': nodeGroup[3],
        'body': "hello3"
    },{
        'startTime': 10,
        'endTime': 20,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[2],
        'receiver': nodeGroup[3],
        'body': "hello4"
    },{
        'startTime': 10,
        'endTime': 21,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[1],
        'receiver': nodeGroup[2],
        'body': "hello4"
    }]
    events=[]
    for paramter in paramtersList:
        events.append(Event(**paramter))
    c=Controller(events,channel)
    c.run()
    logger.output()