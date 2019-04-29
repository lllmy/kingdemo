import pymongo
import os
import redis

# 协议格式：
RET = {
    "code": 0,
    "msg": "",
    "data": {},
}

# 数据配置
mongo_client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MONGO_DB = mongo_client["KingEight"]
REDIS_DB = redis.Redis(host="127.0.0.1",port=6379)

# 资源目录配置
IMAGE_PATH = "Images"
MUSIC_PATH = "Music"
QRCODE_PATH = "QRcode"
CHAT_PATH = "chat"

# 数据采集配置
XPP_URL = "http://m.ximalaya.com/tracks/%s.json"


#创建二维码配置
QR_URL = "http://qr.liantu.com/api.php?text=%s"


#百度AI配置：
APP_ID = '14446007'
API_KEY = 'QrQWLLg5a8qld7Qty7avqCGC'
SECRET_KEY = 'O5mE31LSl17hm8NRYyf9PwlE5Byqm0nr'
from aip import AipSpeech,AipNlp
SPEECH = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
NLP = AipNlp(APP_ID, API_KEY, SECRET_KEY)

#图灵机器人配置：
TULING_URL = "http://openapi.tuling123.com/openapi/api/v2"
