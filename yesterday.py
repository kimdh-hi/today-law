import os
from flask import Flask, render_template, Blueprint
import requests
import datetime
from urllib import parse

bp = Blueprint('yesterday', __name__, url_prefix='/')

app = Flask(__name__)

API_KEY = os.environ['API_KEY']
age = 21


@bp.route('/yesterday', methods=["GET"])
def get_yesterday_info():
    target_date = datetime.datetime.now() - datetime.timedelta(days=1)
    target_date = str(target_date.strftime("%Y-%m-%d"))

    request_url = f"https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?Key={API_KEY}&Type=json&AGE={age}&DT={target_date}"
    query = encode_querystring(request_url)

    data = requests.get("https://open.assembly.go.kr/portal/openapi/nqfvrbsdafrmuzixe?" + query)

    data = data.json()
    total_count = data['nqfvrbsdafrmuzixe'][0]['head'][0]['list_total_count']
    data = data['nqfvrbsdafrmuzixe'][1]['row']

    laws = []

    for d in data:
        title = d['BILL_NM']
        proposer_names = title.split('(')[-1][:-1]
        title = title.split('(')[0]

        doc = {
            "law_id": d['BILL_ID'],
            "title": title,
            "committee": d['COMMITTEE'],
            "status": d['ACT_STATUS'],
            "detail_status": d['STAGE'],
            "url": d['LINK_URL'],
            "proposer_names": proposer_names
        }

        laws.append(doc)

    return render_template('index.html', laws=laws)


def encode_querystring(url):
    url = parse.urlparse(url)
    query = parse.parse_qs(url.query)
    query = parse.urlencode(query, doseq=True)

    return query