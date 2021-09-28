from flask import Blueprint, request, jsonify
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.todaylaw

bp = Blueprint('bookmark', __name__, url_prefix='/')

@bp.route('/api/bookmark', methods=['GET'])
def get_bookmark():
    bookmark_list = list(db.bookmark.find({}, {'_id': False}))
    return jsonify({'bookmark_list':bookmark_list})

# 법안 즐겨찾기
@bp.route('/api/bookmark', methods=['POST'])
def bookmark():
    id_receive = request.form['id_give']
    id = db.ranking.find_one({'id': id_receive})
    point_id = id['id']
    url = id['url']
    title = id['title']
    proposer = id['proposer']
    date = id['date']

    bookmark_id = db.bookmark.find_one({'id': point_id})

    if bookmark_id is not None:
        msg = "이미 즐겨찾기에 저장된 법안입니다."
    else:
        doc = {
            "id": point_id,
            "url": url,
            "title": title,
            "proposer": proposer,
            "date": date
        }

        db.bookmark.insert_one(doc)
        msg = "즐겨찾기에 저장되었습니다."

    return jsonify({'result': 'success', 'msg': f'{msg}'})

# 법안 즐겨찾기 삭제
@bp.route('/api/delete_bookmark', methods=['POST'])
def delete_bookmark():

    id_receive = request.form['id_give']
    bookmark_id = db.bookmark.find_one({'id': id_receive})

    if bookmark_id is not None:
        db.bookmark.delete_one({"id": id_receive})
        msg = "법안이 삭제 되었습니다."
    else:
        msg = "즐겨찾기에 없는 법안입니다."

    return jsonify({'result': 'success', 'msg': f'{msg}'})



