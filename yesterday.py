import os
from flask import render_template, Blueprint, request, jsonify
import requests
import datetime
from urllib import parse

bp = Blueprint('yesterday', __name__, url_prefix='/')

API_KEY = os.environ['API_KEY']
age = 21


@bp.route('/yesterday', methods=['GET'])
def yesterday_page():
    return render_template('yesterday.html')


@bp.route('/api/yesterday', methods=["GET"])
def get_yesterday_info():
    target_date = datetime.datetime.now() - datetime.timedelta(days=1)
    target_date = str(target_date.strftime("%Y-%m-%d"))

    status = request.args.get('status')

    print(status)

    if status is None:
        request_url = f"https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?Key={API_KEY}&Type=json&AGE={age}&DT={target_date}"
        query = encode_querystring(request_url)
    else:
        request_url = f"https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?Key={API_KEY}&Type=json&AGE={age}&DT={target_date}&ACT_STATUS={status}"
        query = encode_querystring(request_url)

    laws = []

    data = requests.get("https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?" + query)
    data = data.json()

    data = data['nqfvrbsdafrmuzixe'][1]['row']

    for d in data:
        title = d['BILL_NM']
        proposer_names = title.split('(')[-1][:-1]
        title = title.split('(')[0]

        doc = {
            "law_id":d['BILL_ID'],
            "title":title,
            "committee":d['COMMITTEE'],
            "status":d['ACT_STATUS'],
            "detail_status":d['STAGE'],
            "url":d['LINK_URL'],
            "proposer_names":proposer_names
        }

        laws.append(doc)

    return jsonify(laws)


def encode_querystring(url):
    url = parse.urlparse(url)
    query = parse.parse_qs(url.query)
    query = parse.urlencode(query, doseq=True)

    return query