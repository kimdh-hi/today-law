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

    doc = {
        "id": point_id,
        "url": url,
        "title": title,
        "proposer": proposer,
        "date": date
    }
    db.bookmark.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'법안 {title} 저장!'})


# 법안 즐겨찾기 삭제
@bp.route('/api/delete_bookmark', methods=['POST'])
def delete_bookmark():

    id_receive = request.form['id_give']
    db.bookmark.delete_one({"id": id_receive})

    return jsonify({'result': 'success', 'msg': f'법안 삭제!'})



