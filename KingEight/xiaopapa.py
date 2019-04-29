import requests,os
from settings import MONGO_DB
from settings import IMAGE_PATH
from settings import MUSIC_PATH
from uuid import uuid4

content_url = "/ertong/424529/7713546"
content_type = "erge"
content_id = content_url.rsplit("/", 1)[-1]
res = requests.get("http://m.ximalaya.com/tracks/%s.json" % (content_id))
content_info = res.json()

content_name = str(uuid4())
content_img_path = os.path.join(IMAGE_PATH,content_name)
content_music_path = os.path.join(MUSIC_PATH,content_name)

audio = requests.get(content_info.get("play_path"))
with open(f"{content_music_path}.mp3", "wb") as f:
    f.write(audio.content)

img = requests.get(content_info.get("cover_url"))
with open(f"{content_img_path}.jpg", "wb") as f:
    f.write(img.content)

title = content_info.get("title")
nickname = content_info.get("nickname")
album_title = content_info.get("album_title")
intro = content_info.get("intro")
play_count = 0

content = {
    "title": title,
    "content_type": content_type,
    "nickname": nickname,
    "album_title": album_title,
    "intro": intro,
    "play_count": play_count,
    "audio": f"{content_name}.mp3",
    "cover": f"{content_name}.jpg"
}

MONGO_DB.content.insert_one(content)
