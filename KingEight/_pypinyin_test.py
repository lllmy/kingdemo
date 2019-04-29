from pypinyin import TONE2,lazy_pinyin
from settings import MONGO_DB

a = lazy_pinyin("园园，圆圆，媛媛，苑苑",style=TONE2)
print(a)
print("".join(a))

# toy_info = MONGO_DB.toys.find()
# for toy in toy_info:
#     for friend in toy["friend_list"]:
#         friend["friend_nickname_pinyin"] = "".join(lazy_pinyin(friend["friend_nickname"], style=TONE2))
#         friend["friend_remark_pinyin"] = "".join(lazy_pinyin(friend["friend_remark"], style=TONE2))
#
#     MONGO_DB.toys.update_one({"_id":toy.get("_id")},{"$set":toy})





