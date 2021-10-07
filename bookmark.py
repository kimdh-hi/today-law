from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import jwt
from decouple import config

client = MongoClient('localhost',27017)
db = client.todaylaw

bp = Blueprint('bookmark', __name__, url_prefix='/')

jwt_secret = config('JWT_SECRET')

# 즐겨찾기 목록 가져오기
@bp.route('/api/bookmark', methods=['GET'])
def get_bookmark():
    try:
        # 토큰 검증
        mytoken = request.cookies.get('mytoken')
        user = verify_token(mytoken)

        # 즐겨찾기 db에서 현재 user의 id에 해당하는 데이터만 가져온다.
        bookmark_list = list(db.bookmark.find(
            {'user_id': user['user_id']}, {'_id':False}
        ))

        return jsonify({'bookmark_list':bookmark_list})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result": "허용되지 않은 접근입니다.", 'bookmark_list':[]})

# 법안 즐겨찾기
@bp.route('/api/bookmark', methods=['POST'])
def bookmark():
    try:
        # jwt 토큰 검증
        mytoken = request.cookies.get('mytoken')
        user = verify_token(mytoken)

        # 즐겨찾기 추가를 위한 파라미터
        law_id = request.form['id_give'] # 즐겨찾기를 한 법안의 ID (API로부터 받은 ID)
        title = request.form['title']
        proposer_name = request.form['proposer_name']
        proposer_names = request.form['proposer_names']
        url = request.form['url']
        date = request.form['date']

        # 즐겨찾기로 추가하려는 법안이 이미 즐겨찾기로 등록되었는지 체크
        exist_id = db.bookmark.find_one({'id': law_id})

        if exist_id is not None:
            msg = "이미 즐겨찾기에 저장된 법안입니다."
        else:
            bookmark_doc = {
                "law_id": law_id,
                "url": url,
                "title": title,
                "proposer_name": proposer_name,
                "proposer_names": proposer_names,
                "date": date,
                "user_id": user['user_id'] # user와 bookmark를 매핑시켜줄 필드 (현재 user의 id값)
            }

            # 즐겨찾기로 추가된 법안의 id를 user의 bookmarks 필드에 추가한다.
            # 이 부분이 필요한지 아직 잘 모르겠음. 마이페이지에서 즐겨찾기를 추가할 때에도 즐겨찾기의 user_id를 사용하면 됨.
            db.users.update(
                {'user_id':user['user_id']},
                {'$push':{'bookmarks':law_id}}
            )
            db.bookmark.insert_one(bookmark_doc)

            msg = "즐겨찾기에 저장되었습니다."
        return jsonify({'result': 'success', 'msg': f'{msg}'})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result":"허용되지 않은 접근입니다."})


# 법안 즐겨찾기 삭제
@bp.route('/api/bookmark', methods=['DELETE'])
def delete_bookmark():
    try:
        # 토큰 검증
        mytoken = request.cookies.get('mytoken')
        user = verify_token(mytoken)

        id_receive = request.form['id_give']
        # 즐겨찾기 db에 있는 지 확인
        bookmark_id = db.bookmark.find_one({'law_id': id_receive, 'user_id':user['user_id']}, {'_id':False})

        if bookmark_id is not None:
            # users DB의 bookmark 필드에서 삭제 (이것도 필요한 부분인지 아직 모르겠음)
            db.users.update(
                {'user_id':user['user_id']},
                {'$pull': {'bookmark_id':id_receive}}
            )
            # bookmark db에서 삭제
            db.bookmark.delete_one({"law_id": id_receive, "user_id":user['user_id']})
            msg = "법안이 삭제 되었습니다."
        else:
            msg = "즐겨찾기에 없는 법안입니다."

        return jsonify({'result': 'success', 'msg': f'{msg}'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({"result":"허용되지 않은 접근입니다."})

# 토큰 검증 메서드
def verify_token(mytoken):
    # 인코딩된 토큰의 payload 부분 디코딩
    token = jwt.decode(mytoken, jwt_secret, algorithms=['HS256'])
    # 디코딩된 payload의 user_id가 users DB에 있는지 확인
    user = db.users.find_one({'user_id': token['user_id']}, {'_id': False})

    return user



