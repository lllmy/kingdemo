from settings import SPEECH, CHAT_PATH, MONGO_DB, TULING_URL
from uuid import uuid4
from bson import ObjectId
from pypinyin import TONE2,lazy_pinyin
import os, requests, json

import jieba
import gensim
from gensim import corpora
from gensim import models
from gensim import similarities


def text2audio(text):
    filename = f"{uuid4()}.mp3"
    file_path = os.path.join(CHAT_PATH, filename)
    res = SPEECH.synthesis(text, options={
        "vol": 8,
        "pit": 8,
        "spd": 5,
        "per": 4
    })

    with open(file_path, "wb") as f:
        f.write(res)

    return filename


def audio2text(filename):
    res = SPEECH.asr(speech=get_file_content(filename), options={
        "dev_pid": 1536,
    })

    return res.get("result")[0]


def get_file_content(filePath):
    cmd_str = f"ffmpeg -y -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm"
    os.system(cmd_str)
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()


def my_nlp_lowb(Q, uid=None):
    ret_dict = {
        "music": "",
        "type": "",
        "to_user": ""
    }

    if "我要听" in Q or "我想听" in Q:
        title,score = my_yuliaoku(Q)
        if score > 0:
            audio = MONGO_DB.content.find_one({"title":title})
            ret_dict["music"] = audio.get("audio")
            ret_dict["type"] = "music"
            return ret_dict

    if "发消息" in Q or "聊聊天" in Q or "说说话" in Q:
        Q_pinyin = "".join(lazy_pinyin(Q,style=TONE2))
        toy_info = MONGO_DB.toys.find_one({"_id": ObjectId(uid)})
        for friend in toy_info.get("friend_list"):
            print(friend.get("friend_remark_pinyin"))
            if friend.get("friend_remark_pinyin") in Q_pinyin or friend.get("friend_nickname_pinyin") in Q_pinyin:
                filename = text2audio(f"可以按消息键，给{friend.get('friend_remark')}发消息了")
                ret_dict["music"] = filename
                ret_dict["type"] = "chat"
                ret_dict["to_user"] = friend.get("friend_id")
                return ret_dict

    ret_dict["music"] = text2audio(goto_tuling(Q, uid))
    ret_dict["type"] = "chat"

    return ret_dict


def goto_tuling(q_text, uid):
    to_tuling_str = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": q_text
            },
        },
        "userInfo": {
            "apiKey": "d4e62f62153641bc81403f51b26d042c",
            "userId": uid
        }
    }
    # xiaobeijiqiren：【今天，北京】
    response = requests.post(TULING_URL, json=to_tuling_str)
    # tuling_res = response.json()
    tuling_res = json.loads(response.content)
    print(tuling_res.get("results")[0]["values"]["text"])
    return tuling_res.get("results")[0]["values"]["text"]

l1 = [content.get("title")  for content in MONGO_DB.content.find({})]
all_doc_list = []
for doc in l1:
    doc_list = [word for word in jieba.cut(doc)]
    all_doc_list.append(doc_list)

dictionary = corpora.Dictionary(all_doc_list)
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
lsi = models.LsiModel(corpus)
index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))

def my_yuliaoku(a):
    doc_test_list = [word for word in jieba.cut(a)]
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    sim = index[lsi[doc_test_vec]]
    cc = sorted(enumerate(sim), key=lambda item: -item[1])

    text = l1[cc[0][0]]

    print(text,cc[0][1])

    return text,cc[0][1]


