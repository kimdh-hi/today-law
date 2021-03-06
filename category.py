import os
from flask import jsonify, request, Blueprint, render_template
from urllib import parse
from pymongo import MongoClient

MONGO_URL = os.environ['MONGO_URL']
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
client = MongoClient(MONGO_URL, 27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)

db = client.todaylaw

bp = Blueprint("category", __name__, url_prefix='/')

# http://localhost:5000/category/test
@bp.route('/category')
def category_view():
    return render_template('categoryList.html')

# http://localhost:5000/api/category?query=조세
@bp.route("/api/category", methods=["GET"])
def get_laws_by_category():
    query = request.args.get('query')
    law_list = list(db.category.find({'category':query}, {'_id':False}))
    for law in law_list:
        if len(law['title']) > 42:
            law['title'] = law['title'][:42] + "..."
    return jsonify(law_list)



# 요청 URL에서 문자열 쿼리스트링 인코딩
def encode_querystring(url):
    url = parse.urlparse(url)
    query = parse.parse_qs(url.query)
    query = parse.urlencode(query, doseq=True)

    return query

def get_other_proposer(names):
    names = names.split(',')
    names_len = len(names)
    names = ','.join(names[:10])
    if names_len > 10:
        extra = names_len - 10
        names = names + f' 외 {extra}명'
    return names