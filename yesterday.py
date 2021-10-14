import os
from flask import render_template, Blueprint, request
import requests
import datetime
from urllib import parse

bp = Blueprint('yesterday', __name__, url_prefix='/')

API_KEY = os.environ['API_KEY']
age = 21


@bp.route('/yesterday', methods=["GET"])
def get_yesterday_info():
    target_date = datetime.datetime.now() - datetime.timedelta(days=1)
    target_date = str(target_date.strftime("%Y-%m-%d"))

    status = request.args.get('status')

    if status is None:
        request_url = f"https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?Key={API_KEY}&Type=json&AGE={age}&DT={target_date}"
        query = encode_querystring(request_url)
    else:
        request_url = f"https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?Key={API_KEY}&Type=json&AGE={age}&DT={target_date}&ACT_STATUS={status}"
        query = encode_querystring(request_url)

    laws = []

    data = requests.get("https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?" + query)
    data = data.json()

    try:
        if data['RESULT']['MESSAGE'] == "해당하는 데이터가 없습니다.":
            return render_template('yesterday.html', laws=laws)
    except (KeyError):
        total_count = data['nqfvrbsdafrmuzixe'][0]['head'][0]['list_total_count']
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

    return render_template('yesterday.html', laws=laws)


def encode_querystring(url):
    url = parse.urlparse(url)
    query = parse.parse_qs(url.query)
    query = parse.urlencode(query, doseq=True)

    return query