import zmq
import os
from twilio.rest import Client
import threading
import requests


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code






def messager(port):
# send message with twilio via whats app
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    address = "tcp://localhost:" + str(port)
    socket.connect(address)

    #  Do 10 requests, waiting each time for a response
    while (True):
        socket.send(b"connected")
        print(str(port) + " connected to mt4")
        #  Get the reply.
        mt4_message = socket.recv()
        content = str(mt4_message)

        message = content
        token = 'Tc0FF0uHSQr2r7HXPbE9GSe7bssJVoxezZrkg9jtHzV'
        lineNotifyMessage(token, message)
        print(content)


t1 = threading.Thread(target=messager, name="thread5555",args = (5555,))
t2 = threading.Thread(target=messager, name="thread5556",args = (5556,))
t3 = threading.Thread(target=messager, name="thread5557",args = (5557,))
t4 = threading.Thread(target=messager, name="thread5558",args = (5558,))
t5 = threading.Thread(target=messager, name="thread5559",args = (5559,))
t6 = threading.Thread(target=messager, name="thread5560",args = (5560,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
