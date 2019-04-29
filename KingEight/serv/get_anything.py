from flask import Blueprint, request, jsonify, send_file
from settings import IMAGE_PATH, MUSIC_PATH, CHAT_PATH, RET, MONGO_DB
from bson import ObjectId
from uuid import uuid4
from baidu_aip import baidu_asr_sync
import os

get_any = Blueprint("get_any", __name__)


@get_any.route("/get_music/<filename>")
def get_music(filename):
    filename = os.path.join(MUSIC_PATH, filename)
    return send_file(filename)


@get_any.route("/get_chat/<filename>")
def get_chat(filename):
    filename = os.path.join(CHAT_PATH, filename)
    return send_file(filename)


@get_any.route("/get_image/<filename>")
def get_image(filename):
    filename = os.path.join(IMAGE_PATH, filename)
    return send_file(filename)


@get_any.route("/uploder", methods=["POST"])
def uploder():
    record_file = request.files.get("record")
    chat_window = request.form.get("chat_window")
    user_id = request.form.get("user_id")
    # <FileStorage: '1540266751978.amr' ('audio/amr')>
    record_path = os.path.join(CHAT_PATH, record_file.filename)
    record_file.save(record_path)
    os.system(f"ffmpeg -i {record_path} {record_path}.mp3")

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = {}

    # chat = MONGO_DB.chat.find_one({"_id":ObjectId(chat_window)})
    # chat["chat_list"].append({})
    sender_msg = {
        "sender": user_id,
        "msg": f"{record_file.filename}.mp3"
    }
    MONGO_DB.chat.update_one({"_id": ObjectId(chat_window)}, {"$push": {"chat_list": sender_msg}})

    return jsonify(RET)


@get_any.route("/toy_uploader", methods=["POST"])
def toy_uploader():
    file_name = f"{uuid4()}.wav"
    record_file = request.files.get("record")
    sender = request.form.get("sender")
    to_user = request.form.get("to_user")
    record_path = os.path.join(CHAT_PATH, file_name)
    record_file.save(record_path)

    sender_msg = {
        "sender": sender,
        "msg": file_name
    }
    MONGO_DB.chat.update_one({"user_list": {"$all": [sender, to_user]}}, {"$push": {"chat_list": sender_msg}})

    return jsonify({"code": 0})


@get_any.route("/toy_ai", methods=["POST"])
def toy_ai():
    file_name = f"{uuid4()}.wav"
    record_file = request.files.get("record")
    sender = request.form.get("sender")
    print(sender)
    # to_user = request.form.get("to_user")
    record_path = os.path.join(CHAT_PATH, file_name)
    record_file.save(record_path)

    text = baidu_asr_sync.audio2text(record_path)
    print(text)
    ret_dict = baidu_asr_sync.my_nlp_lowb(text,sender)

    return jsonify(ret_dict)