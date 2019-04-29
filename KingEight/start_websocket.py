from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from baidu_aip import baidu_asr_sync
from settings import MONGO_DB,REDIS_DB
from bson import ObjectId
import json


websocket_app = Flask(__name__)

user_socket_dict = {}


@websocket_app.route("/ws/<uid>")
def ws(uid):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    user_socket_dict[uid] = user_socket
    print(len(user_socket_dict), user_socket_dict)
    while True:
        msg = user_socket.receive()
        print(msg)
        msg_dict = json.loads(msg)  # {to_user:toy_id,chat:abc.mp3}
        to_user = msg_dict.get("to_user")
        to_user_socket = user_socket_dict.get(to_user)

        msg = send_msg(uid,to_user)

        if msg_dict.get("chat"):
            send_something = {"msg_type": "chat", "msg": msg ,"from_user":uid}
            print(uid,to_user)
            set_redis(uid,to_user)

        if msg_dict.get("music"):
            send_something = {"msg_type": "music", "msg": msg_dict.get("music")}

        # send_something = msg_dict.get("music") if msg_dict.get("music") else msg_dict.get("chat")
        if to_user_socket:
            to_user_socket.send(json.dumps(send_something))


@websocket_app.route("/toy_ws/<uid>")
def toy_ws(uid):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    user_socket_dict[uid] = user_socket
    print(len(user_socket_dict), user_socket_dict)
    while True:
        msg = user_socket.receive()
        print(msg)
        msg_dict = json.loads(msg)  # {to_user:123}
        to_user = msg_dict.get("to_user")
        user = MONGO_DB.users.find_one({"_id":ObjectId(to_user)})
        if user:
            user_type = "user"
        else:
            user_type = "toy"

        to_user_socket = user_socket_dict.get(to_user)

        #玩具收消息 玩具与玩具之间的对话


        if to_user_socket:
            print(user_type)
            if user_type == "user":
                send_str = json.dumps({"sender": uid})
                set_redis(uid, to_user)
                to_user_socket.send(send_str)
            else:
                msg = send_msg(uid, to_user)
                set_redis(uid, to_user)
                send_something = {"msg_type": "chat", "msg": msg, "from_user": uid}
                print(uid, to_user)
                to_user_socket.send(json.dumps(send_something))



def set_redis(sender,to_user):
    user_msg = REDIS_DB.get(to_user)
    if not user_msg:
        REDIS_DB.set(to_user, json.dumps({sender: 1}))
    else:
        user_msg = json.loads(user_msg)
        if not user_msg.get(sender):
            user_msg[sender] = 1

        else:
            user_msg[sender] += 1

        REDIS_DB.set(to_user, json.dumps(user_msg))



def send_msg(sender, to_user): # to_user 一定是玩具
    print(sender,to_user)
    to_user_info = MONGO_DB.toys.find_one({"_id": ObjectId(to_user)})
    for friend in to_user_info.get("friend_list"):
        print(friend)
        if friend.get("friend_id") == sender:
            remark = friend.get("friend_remark")  # 爸爸
            msg = baidu_asr_sync.text2audio(f"你有来自{remark}的消息")
            return msg


if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 9528), websocket_app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
