from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.todaylaw

bp = Blueprint('wish', __name__, url_prefix='/')


@bp.route('/wish', methods=['GET'])
def show_wish():
    wish_list = list(db.wish.find({}, {'_id': False}).sort([('_id',-1)]))
    return jsonify({'wish_list': wish_list})


@bp.route('/wish', methods=['POST'])
def save_wish():
    title_receive = request.form['title_give']
    category_receive = request.form['category_give']
    contents_receive = request.form['contents_give']

    today = datetime.now()
    nowtime = today.strftime('%Y-%m-%d')

    wish_doc = {
        "title": title_receive,
        "category": category_receive,
        "contents": contents_receive,
        "time": nowtime,
        "agree": 0
    }
    db.wish.insert_one(wish_doc)
    return jsonify({'msg': '저장완료'})
