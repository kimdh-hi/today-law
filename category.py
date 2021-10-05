from flask import Flask, jsonify, request, Blueprint, render_template
import requests
from urllib import parse
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text

bp = Blueprint("category", __name__, url_prefix='/')

age = 21
type = 'json'
g_categories = [
    {"건설":      ["건설", "공항", "도로", "철도", "항만", "주택"]},
    {"노동":      ["노동", "일자리"]},
    {"문화":      ["문화", "스포츠", "음악", "게임"]},
    {"부동산":     ["부동산"]},
    {"범죄":      ["범죄", "피해자", "성폭력", "학대", "폭력", "처벌"]},
    {"의료/보건":  ["의료", "보건", "건강", "병원", "의사", "간호", "의약"]}
]

# http://localhost:5000/category/test
@bp.route('/category')
def category_view():
    return render_template('categoryList.html')

# http://localhost:5000/api/category?category=조세
@bp.route("/api/category", methods=["GET"])
def get_laws_by_category():
    list_count = 0
    category = request.args.get('category')
    categories = []
    for g_category in g_categories:
        if g_category.get(category) is not None:
            tmp_category_list = g_category.get(category)
            for tmp in tmp_category_list:
                categories.append(tmp)

    response = []
    list_count = 0
    for category_name in categories:
        url = f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}&BILL_NAME={category_name}&pIndex=1&pSize=50'
        query = encode_querystring(url)
        data = requests.get('https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?' + query)

        data = data.json()
        total_count = data['nzmimeepazxkubdpn'][0]['head'][0]['list_total_count']
        print(total_count)

        data = data['nzmimeepazxkubdpn'][1]['row']

        for d in data:
            list_count+=1
            names = d['PUBL_PROPOSER']

            response.append({
                'title': d['BILL_NAME'],  # 법안제목
            })
            if list_count >= 50:
                print('ret ', list_count)
                return jsonify(response)

    return jsonify(response)



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