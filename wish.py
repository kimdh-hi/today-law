from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from decouple import config
import jwt

host = config('MONGO_DB_CLIENT')
client = MongoClient(host, 27017)
db = client.todaylaw

bp = Blueprint('wish', __name__, url_prefix='/')

jwt_secret = config('JWT_SECRET')

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
        mytoken = request.cookies.get('mytoken')
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

def verify_token(mytoken):
    # 인코딩된 토큰의 payload 부분 디코딩
    token = jwt.decode(mytoken, jwt_secret, algorithms=['HS256'])
    # 디코딩된 payload의 user_id가 users DB에 있는지 확인
    user = db.users.find_one({'user_id': token['user_id']}, {'_id': False})

    return user
