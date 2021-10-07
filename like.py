from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import jwt
from decouple import config
client = MongoClient('localhost',27017)
db = client.todaylaw

bp = Blueprint('like', __name__, url_prefix='/')

jwt_secret = config('JWT_SECRET')

@bp.route('/api/like', methods=['POST'])
def like_star():
    try:
        # 토큰 검증
        mytoken = request.cookies.get('mytoken')
        user = verify_token(mytoken)

        id_receive = request.form['id_give']

        like_laws = db.users.find_one(
            {'user_id':user['user_id']},
            {'like_laws':1, '_id':0}
        )['like_laws']

        if id_receive in like_laws: # 좋아요가 이미 눌린 법안인 경우
            # 사용자의 좋아요 목록에서 제거
            db.users.update(
                {'user_id':user['user_id']},
                {'$pull':{'like_laws':id_receive}}
            )

            # 좋아요를 감소시키는 부분
            likes = db.ranking.find_one({'id': id_receive})
            current_like = likes['like']
            new_like = current_like - 1
            current_hate = likes['hate']
            db.ranking.update_one({'id': id_receive}, {'$set': {'like': new_like}})
        else: # 좋아요가 처음 눌린 법안인 경우
            # 사용자의 좋아요 목록에 추가
            db.users.update(
                {'user_id': user['user_id']},
                {'$push': {'like_laws': id_receive}}
            )

            # 좋아요를 증가시키는 부분
            likes = db.ranking.find_one({'id': id_receive})
            current_like = likes['like']
            new_like = current_like + 1
            current_hate = likes['hate']
            db.ranking.update_one({'id': id_receive}, {'$set': {'like': new_like}})

        return jsonify({'id': id_receive, 'like': new_like, 'hate': current_hate})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})


@bp.route('/api/hate', methods=['POST'])
def delete_star():
    try:
        # 토큰 검증
        mytoken = request.cookies.get('mytoken')
        user = verify_token(mytoken)

        id_receive = request.form['id_give']

        hate_laws = db.users.find_one(
            {'user_id': user['user_id']},
            {'hate_laws': 1, '_id': 0}
        )['hate_laws']

        if id_receive in hate_laws:
            db.users.update(
                {'user_id': user['user_id']},
                {'$pull': {'hate_laws': id_receive}}
            )

            hates = db.ranking.find_one({'id': id_receive})
            current_hate = hates['hate']
            new_hate = current_hate - 1
            current_like = hates['like']
            db.ranking.update_one({'id': id_receive}, {'$set': {'hate': new_hate}})
        else:  # 좋아요가 처음 눌린 법안인 경우
            # 사용자의 좋아요 목록에 추가
            db.users.update(
                {'user_id': user['user_id']},
                {'$push': {'hate_laws': id_receive}}
            )

            hates = db.ranking.find_one({'id': id_receive})
            current_hate = hates['hate']
            new_hate = current_hate + 1
            current_like = hates['like']
            db.ranking.update_one({'id': id_receive}, {'$set': {'hate': new_hate}})

        return jsonify({'id': id_receive, 'like': current_like, 'hate':new_hate})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다."})


@bp.route('/api/likes_list', methods=['GET'])
def show_like_list():
    likes_list = list(db.ranking.find({}, {'_id': False}).sort([('like',-1), ('title',1)]).limit(50))
    return jsonify({'likes_list': likes_list})

# 토큰 검증 메서드
def verify_token(mytoken):
    # 인코딩된 토큰의 payload 부분 디코딩
    token = jwt.decode(mytoken, jwt_secret, algorithms=['HS256'])
    # 디코딩된 payload의 user_id가 users DB에 있는지 확인
    user = db.users.find_one({'user_id': token['user_id']}, {'_id': False})

    return user