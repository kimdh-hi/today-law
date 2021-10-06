from flask import jsonify, request, Blueprint, render_template
from urllib import parse
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text
from pymongo import MongoClient

client = MongoClient('localhost',27017)
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