from Controller import Controller
from Models import Event,Node,Channel
from logger import Logger
import Models
import random
if __name__ == '__main__':
    channel=Channel(0)
    nodeGroup=[
        Node(0,random.randint(1,100),random.randint(1,100),channel),
        Node(1,random.randint(1,100),random.randint(1,100),channel),
        Node(2,random.randint(1,100),random.randint(1,100),channel),
        Node(3,random.randint(1,100),random.randint(1,100),channel),
        Node(4, random.randint(1,100), random.randint(1,100), channel),
        Node(5, random.randint(1,100), random.randint(1,100), channel),
        Node(6, random.randint(1,100), random.randint(1,100), channel),
        Node(7, random.randint(1,100), random.randint(1,100), channel),
        Node(8, random.randint(1,100),random.randint(1,100), channel),
        Node(9,random.randint(1,100), random.randint(1,100), channel),
        Node(10,random.randint(1,100), random.randint(1,100), channel),
        Node(11, random.randint(1,100),random.randint(1,100), channel),
        Node(12, random.randint(1,100), random.randint(1,100), channel),
        Node(13, random.randint(1,100), random.randint(1,100), channel),
        Node(14, random.randint(1,100), random.randint(1,100), channel),
        Node(15, random.randint(1,100), random.randint(1,100), channel),
        Node(16, random.randint(1,100), random.randint(1,100), channel),
        Node(17, random.randint(1,100),random.randint(1,100), channel),
        Node(18, random.randint(1,100), random.randint(1,100), channel),
        Node(19, random.randint(1,100), random.randint(1,100), channel),
        Node(20, random.randint(1,100), random.randint(1,100), channel)
    ]
    channel.addGroup(nodeGroup)
    logger=Logger()
    paramtersList=[
        {'startTime':0,
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
    },
    {
        'startTime': 7,
        'endTime': 9,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[4],
        'receiver': nodeGroup[10],
        'body': "hello4"
    },{
        'startTime': 7,
        'endTime': 10,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[5],
        'receiver': nodeGroup[13],
        'body': "hello5"
    }
    ,{
        'startTime': 7,
        'endTime': 11,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[6],
        'receiver': nodeGroup[2],
        'body': "hello6"
    },
    {
        'startTime': 17,
        'endTime': 21,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[7],
        'receiver': nodeGroup[2],
        'body': "hello7"
    },{
        'startTime': 17,
        'endTime': 20,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[8],
        'receiver': nodeGroup[20],
        'body': "hello8"
    },{
        'startTime': 25,
        'endTime': 27,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[11],
        'receiver': nodeGroup[5],
        'body': "hello9"
    },{
        'startTime': 25,
        'endTime': 28,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[12],
        'receiver': nodeGroup[19],
        'body': "hello10"
    },{
        'startTime': 25,
        'endTime': 27,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[13],
        'receiver': nodeGroup[1],
        'body': "hello11"
    },{
        'startTime': 34,
        'endTime': 35,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[14],
        'receiver': nodeGroup[20],
        'body': "hello12"
    },{
        'startTime': 34,
        'endTime': 35,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[15],
        'receiver': nodeGroup[2],
        'body': "hello13"
    },{
        'startTime': 34,
        'endTime': 35,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[16],
        'receiver': nodeGroup[1],
        'body': "hello14"
    },{
        'startTime': 38,
        'endTime': 39,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[17],
        'receiver': nodeGroup[20],
        'body': "hello15"
    },{
        'startTime': 38,
        'endTime': 40,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[18],
        'receiver': nodeGroup[2],
        'body': "hello16"
    },{
        'startTime': 42,
        'endTime': 45,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[19],
        'receiver': nodeGroup[2],
        'body': "hello17"
    },{
        'startTime': 42,
        'endTime': 46,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[20],
        'receiver': nodeGroup[20],
        'body': "hello18"
    },{
        'startTime': 50,
        'endTime': 51,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[0],
        'receiver': nodeGroup[16],
        'body': "hello19"
    },{
        'startTime': 52,
        'endTime': 54,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[1],
        'receiver': nodeGroup[20],
        'body': "hello20"
    },{
        'startTime': 52,
        'endTime': 55,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[2],
        'receiver': nodeGroup[2],
        'body': "hello21"
    },{
        'startTime': 52,
        'endTime': 55,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[3],
        'receiver': nodeGroup[20],
        'body': "hello22"
    },{
        'startTime': 63,
        'endTime': 65,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[4],
        'receiver': nodeGroup[19],
        'body': "hello23"
    },{
        'startTime':63,
        'endTime': 65,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[5],
        'receiver': nodeGroup[18],
        'body': "hello24"
    },{
        'startTime':  63,
        'endTime':67,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[6],
        'receiver': nodeGroup[17],
        'body': "hello25"
    },{
        'startTime': 72,
        'endTime': 75,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[7],
        'receiver': nodeGroup[16],
        'body': "hello26"
    },{
        'startTime':  72,
        'endTime': 73,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[8],
        'receiver': nodeGroup[15],
        'body': "hello27"
    },{
        'startTime': 80,
        'endTime': 82,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[9],
        'receiver': nodeGroup[4],
        'body': "hello28"
    },{
        'startTime':  80,
        'endTime': 81,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[10],
        'receiver': nodeGroup[13],
        'body': "hello29"
    },{
        'startTime':  84,
        'endTime': 86,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[11],
        'receiver': nodeGroup[20],
        'body': "hello30"
    },{
        'startTime':  84,
        'endTime': 87,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[12],
        'receiver': nodeGroup[19],
        'body': "hello31"
    },{
        'startTime':  102,
        'endTime': 106,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[13],
        'receiver': nodeGroup[14],
        'body': "hello32"
    },{
        'startTime':  102,
        'endTime': 108,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[14],
        'receiver': nodeGroup[15],
        'body': "hello33"
    },{
        'startTime': 110,
        'endTime': 111,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[15],
        'receiver': nodeGroup[20],
        'body': "hello34"
    },{
        'startTime': 110,
        'endTime': 115,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[16],
        'receiver': nodeGroup[11],
        'body': "hello35"
    },{
        'startTime': 131,
        'endTime': 135,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[17],
        'receiver': nodeGroup[18],
        'body': "hello36"
    },{
        'startTime': 132,
        'endTime':136,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[18],
        'receiver': nodeGroup[19],
        'body': "hello37"
    },{
        'startTime': 135,
        'endTime': 136,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[19],
        'receiver': nodeGroup[10],
        'body': "hello38"
    },{
        'startTime': 160,
        'endTime': 161,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[20],
        'receiver': nodeGroup[2],
        'body': "hello39"
    },{
        'startTime': 162,
        'endTime': 165,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[0],
        'receiver': nodeGroup[12],
        'body': "hello40"
    },{
        'startTime': 176,
        'endTime': 178,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[1],
        'receiver': nodeGroup[19],
        'body': "hello41"
    },{
        'startTime':176,
        'endTime': 179,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[2],
        'receiver': nodeGroup[0],
        'body': "hello42"
    },{
        'startTime': 176,
        'endTime': 181,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[3],
        'receiver': nodeGroup[1],
        'body': "hello43"
    },{
        'startTime': 182,
        'endTime': 185,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[4],
        'receiver': nodeGroup[17],
        'body': "hello44"
    },{
        'startTime': 182,
        'endTime': 183,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[5],
        'receiver': nodeGroup[2],
        'body': "hello45"
    },{
        'startTime': 282,
        'endTime': 285,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[6],
        'receiver': nodeGroup[1],
        'body': "hello46"
    },{
        'startTime': 320,
        'endTime': 325,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[7],
        'receiver': nodeGroup[17],
        'body': "hello47"
    },{
        'startTime': 320,
        'endTime': 331,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[8],
        'receiver': nodeGroup[20],
        'body': "hello48"
    },{
        'startTime': 331,
        'endTime': 321,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[9],
        'receiver': nodeGroup[11],
        'body': "hello49"
    },{
        'startTime': 322,
        'endTime': 331,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[10],
        'receiver': nodeGroup[2],
        'body': "hello50"
    },{
        'startTime': 322,
        'endTime': 335,
        'code': Models.MESSAGE_EVENT,
        'sender': nodeGroup[18],
        'receiver': nodeGroup[17],
        'body': "hello51"
    }
    ]
    events=[]
    for paramter in paramtersList:
        events.append(Event(**paramter))
    c=Controller(events,channel)
    c.run()
    logger.output()