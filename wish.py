import os
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import jwt

MONGO_URL = os.environ['MONGO_URL']
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
client = MongoClient(MONGO_URL, 27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)

db = client.todaylaw

bp = Blueprint('wish', __name__, url_prefix='/')

TOKEN_KEY = os.environ['TOKEN_KEY']
JWT_SECRET = os.environ['JWT_SECRET']

# 청원 목록 가져오기
# 로그인 하지 않아도 보여야 함
@bp.route('/wish', methods=['GET'])
def show_wish():
    wish_list = list(db.wish.find({}, {'_id': False}).sort([('_id', -1)]))
    return jsonify({'wish_list': wish_list})


# 청원 등록하기
@bp.route('/wish', methods=['POST'])
def save_wish():
    try:
        mytoken = request.cookies.get(TOKEN_KEY)
        user = verify_token(mytoken)

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
            "agree": 0,
            "user_id": user['user_id']
        }
        db.wish.insert_one(wish_doc)
        return jsonify({'result': 'success', 'msg': '저장완료'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})

# 청원 상세페이지
@bp.route('/wish/details', methods=['POST'])
def show_wish_details():
    title = request.form['title_give']
    category = request.form['category_give']
    time = request.form['time_give']
    agree = request.form['agree_give']
    contents = request.form['contents_give']

    return jsonify({'category': category, 'title': title, 'agree': agree,
                    'time': time, 'contents': contents})

# 청원 댓글
@bp.route('/wish/comment', methods=['POST'])
def save_wish_comment():
    title_receive = request.form['title_give']
    agrees = db.wish.find_one({'title': title_receive})
    current_agree = agrees['agree']
    new_agree = current_agree + 1

    db.wish.update_one({'title': title_receive}, {'$set': {'agree': new_agree}})
    return jsonify({'result': 'success', 'msg': '동의완료'})



def verify_token(mytoken):
    # 인코딩된 토큰의 payload 부분 디코딩
    token = jwt.decode(mytoken, JWT_SECRET, algorithms=['HS256'])
    # 디코딩된 payload의 user_id가 users DB에 있는지 확인
    user = db.users.find_one({'user_id': token['user_id']}, {'_id': False})

    return user
