from flask import Blueprint, request, jsonify, send_file
from settings import MONGO_DB, RET
from bson import ObjectId

fri = Blueprint("fri", __name__)


@fri.route("/friend_list", methods=["POST"])
def friend_list():
    user_id = request.form.get("user_id")
    res = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    friend_list = res.get("friend_list")

    RET["code"] = 0
    RET["msg"] = "获取好友列表"
    RET["data"] = friend_list

    return jsonify(RET)


@fri.route("/add_req", methods=["POST"])
def add_req():
    toy_id = request.form.get("toy_id")
    add_toy_id = request.form.get("add_toy_id")
    req_content = request.form.get("req_content")
    scan_type = request.form.get("scan_type")
    remark = request.form.get("remark")

    if scan_type == "user":
        user_info = MONGO_DB.users.find_one({"_id": ObjectId(toy_id)})
    else:
        user_info = MONGO_DB.toys.find_one({"_id": ObjectId(toy_id)})

    # {谁id ， 加谁id ，请求内容 ，请求状态1 ，谁头像，谁名字}
    request_content = {
        "user": toy_id,
        "add_toy_id": add_toy_id,
        "remark": remark,
        "req_content": req_content,
        "status": 1,
        "scan_type": scan_type,
        "user_avatar": user_info.get("avatar"),
        "user_name": user_info.get("nickname") if user_info.get("nickname") else user_info.get("baby_name")
    }

    MONGO_DB.request.insert_one(request_content)

    RET["code"] = 0
    RET["msg"] = "请求发送成功"
    RET["data"] = {}

    return jsonify(RET)


@fri.route("/acc_req", methods=["POST"])
def acc_req():
    req_id = request.form.get("req_id")
    acc_remark = request.form.get("remark")
    req_info = MONGO_DB.request.find_one({"_id": ObjectId(req_id)})

    user_id = req_info.get("user")
    add_toy_id = req_info.get("add_toy_id")
    scan_type = req_info.get("scan_type")
    remark = req_info.get("remark")

    if scan_type == "user":
        user = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
        toy = MONGO_DB.toys.find_one({"_id": ObjectId(add_toy_id)})

        chat_window = MONGO_DB.chat.insert_one({"user_list": [str(toy.get("_id")), str(user.get("_id"))]})

        user["friend_list"].append(
            {
                "friend_nickname": toy.get("baby_name"),
                "friend_avatar": toy.get("avatar"),
                "friend_remark": remark,
                "friend_chat": str(chat_window.inserted_id),
                "friend_id": str(toy.get("_id"))
            }
        )

        toy["friend_list"].append(
            {
                "friend_nickname": user.get("baby_name"),
                "friend_avatar": user.get("avatar"),
                "friend_remark": acc_remark,
                "friend_chat": str(chat_window.inserted_id),
                "friend_id": str(user.get("_id"))
            }
        )

        MONGO_DB.users.update_one({"_id": ObjectId(user_id)}, {"$set": user})
        MONGO_DB.toys.update_one({"_id": ObjectId(add_toy_id)}, {"$set": toy})

        MONGO_DB.request.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": 2}})

        RET["code"] = 0
        RET["msg"] = "已添加好友"
        RET["data"] = {}

        return jsonify(RET)

    else:
        user = MONGO_DB.toys.find_one({"_id": ObjectId(user_id)})
        toy = MONGO_DB.toys.find_one({"_id": ObjectId(add_toy_id)})

        chat_window = MONGO_DB.chat.insert_one({"user_list": [str(toy.get("_id")), str(user.get("_id"))]})

        user["friend_list"].append(
            {
                "friend_nickname": toy.get("baby_name"),
                "friend_avatar": toy.get("avatar"),
                "friend_remark": remark,
                "friend_chat": str(chat_window.inserted_id),
                "friend_id": str(toy.get("_id"))
            }
        )

        toy["friend_list"].append(
            {
                "friend_nickname": user.get("baby_name"),
                "friend_avatar": user.get("avatar"),
                "friend_remark": acc_remark,
                "friend_chat": str(chat_window.inserted_id),
                "friend_id": str(user.get("_id"))
            }
        )

        MONGO_DB.toys.update_one({"_id": ObjectId(user_id)}, {"$set": user})
        MONGO_DB.toys.update_one({"_id": ObjectId(add_toy_id)}, {"$set": toy})

        MONGO_DB.request.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": 2}})

        RET["code"] = 0
        RET["msg"] = "已添加好友"
        RET["data"] = {}

        return jsonify(RET)


@fri.route("/ref_req", methods=["POST"])
def ref_req():
    req_id = request.form.get("req_id")
    MONGO_DB.request.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": 3}})

    RET["code"] = 0
    RET["msg"] = "已拒绝好友请求"
    RET["data"] = {}

    return jsonify(RET)


@fri.route("/req_list", methods=["POST"])
def req_list():
    user_id = request.form.get("user_id")
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    res = list(MONGO_DB.request.find({"add_toy_id": {"$in": user_info.get("bind_toys")}}))
    for index, req in enumerate(res):
        res[index]["_id"] = str(req["_id"])

    RET["code"] = 0
    RET["msg"] = "查看好友请求"
    RET["data"] = res

    return jsonify(RET)
