from flask import Blueprint, request, jsonify
from settings import MONGO_DB
import pymongo
from bson import ObjectId

content_bp = Blueprint("content_bp", __name__)


@content_bp.route("/content_list", methods=["POST"])
def content_list():
    res = list(MONGO_DB.content.find({}))
    for index, item in enumerate(res):
        res[index]["_id"] = str(item["_id"])

    return jsonify(res)


# @content_bp.route("/content_one", methods=["POST"])
# def content_one():
#     content_id = request.form.get("content_id")
#     res = MONGO_DB.content.find_one({"_id": ObjectId(content_id)})
#     res["_id"] = str(res["_id"])
#
#     return jsonify(res)
