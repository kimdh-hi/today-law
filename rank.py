from flask import Blueprint, request, jsonify
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.todaylaw

bp = Blueprint('ranking', __name__, url_prefix='/')

@bp.route('/api/rank', methods=["GET"])
def get_ranking():
    rank_list = db.ranking.find({}).sort([('count',-1)]).limit(5)
    rank_result = []

    for idx, rank in enumerate(rank_list):
        doc = {
            'rank':idx+1,
            'title':rank['title'],
            'count':rank['count']
        }
        rank_result.append(doc)
    print(rank_result)
    return jsonify(rank_result)

@bp.route('/api/rank', methods=['POST'])
def increase_click_count():
    # 법안ID, 법안제목
    id = request.form['id']
    title = request.form['title']

    count = db.ranking.find_one({'id':id}, {'_id':0, 'title':0, 'id':0})
    if count is not None:
        count = count['count']
        new_count = count+1
        db.ranking.update_one({'id':id}, {'$set':{'count':new_count}})
    else:
        doc = {
            'id':id,
            'title':title,
            'count':1
        }
        db.ranking.insert_one(doc)

    return jsonify({'result':'success'})


