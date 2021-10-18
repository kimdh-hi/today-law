import os
import jwt
from flask import Blueprint, request, jsonify, render_template, redirect
from pymongo import MongoClient

MONGO_URL = os.environ['MONGO_URL']
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
# client = MongoClient(MONGO_URL, 27017)
client = MongoClient(MONGO_URL, 27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)
TOKEN_KEY = os.environ['TOKEN_KEY']
JWT_SECRET = os.environ['JWT_SECRET']

db = client.todaylaw

bp = Blueprint('mypage', __name__, url_prefix='/')


@bp.route('/mypage')
def index():
    return render_template('mypage.html')


@bp.route('/mypage2')
def index2():
    return render_template('mypage2.html')


@bp.route('/mypage/wishlist', methods=['GET'])
def wishlist():
    try:
        mytoken = request.cookies.get(TOKEN_KEY)
        user = verify_token(mytoken)

        wishlist = list(db.wish.find({'user_id': user['user_id']}, {'_id': False}))

        title = wishlist[0]['title']
        category = wishlist[0]['category']
        time = wishlist[0]['time']
        agree = wishlist[0]['agree']
        contents = wishlist[0]['contents']

        return jsonify({'result': 'success', 'title_give': title, 'category_give': category, 'time_give': time,
                        'agree_give': agree, 'contents_give': contents})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})


@bp.route('/mypage', methods=['GET'])
def showprofile():
    try:
        mytoken = request.cookies.get(TOKEN_KEY)
        user = verify_token(mytoken)

        user = db.users.find_one({'user_id': user['user_id']}, {'_id': False})

        return jsonify({'result': 'success'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})


@bp.route('/mypage/agree', methods=['POST'])
def agree():
    try:
        mytoken = request.cookies.get(TOKEN_KEY)
        user = verify_token(mytoken)

        user = db.users.find_one({'user_id': user['user_id']}, {'_id': False})

        if user['receive_mail'] == 1:
            db.users.update(
                {'user_id': user['user_id']},
                {'$set': {'receive_mail': 0}}, upsert=True
            )
            msg = '알림이 해제되었습니다.'
        else:
            db.users.update(
                {'user_id': user['user_id']},
                {'$set': {'receive_mail': 1}}, upsert=True
            )
            msg = '알림이 설정되었습니다.'

        return jsonify({'result': msg})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})


@bp.route('/mypage/profile', methods=['POST'])
def edit_profile():
    try:
        mytoken = request.cookies.get(TOKEN_KEY)
        user = verify_token(mytoken)

        user = db.users.find_one({'user_id': user['user_id']}, {'_id': False})

        name_receive = request.form['name_give']
        bio_receive = request.form['bio_give']

        if user['name']==db.user.find_one({'name': name_receive}) or (db.user.find_one({'name': name_receive})) == None:
            db.users.update(
                {'user_id': user['user_id']},
                {'$set': {'name': name_receive, 'bio': bio_receive}}, upsert=True
            )
            result = 'success'
        else:
            result = 'fail'


        return jsonify({'result': result})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})


def verify_token(mytoken):
    # 인코딩된 토큰의 payload 부분 디코딩
    token = jwt.decode(mytoken, JWT_SECRET, algorithms=['HS256'])
    # 디코딩된 payload의 user_id가 users DB에 있는지 확인
    user = db.users.find_one({'user_id': token['user_id']}, {'_id': False})

    return user
