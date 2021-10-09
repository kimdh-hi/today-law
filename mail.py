from flask import Blueprint, request, jsonify
import requests
from pymongo import MongoClient
from decouple import config
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from pymongo import MongoClient
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text

client = MongoClient('localhost',27017)
db = client.todaylaw

bp = Blueprint("mail_send_scheduler", __name__, url_prefix='/')

age = 21
type = 'json'

# 발의된 날짜가 어제인 법안을 받아온다.
@bp.route('/test/mail', methods=["GET"])
def get_laws():
    flag = True
    while flag:
        url = f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}&pIndex=1&pSize=50'
        data = requests.get(url).json()
        data = data['nzmimeepazxkubdpn'][1]['row']

        law_list = []

        for d in data:
            propose_date = str(d['PROPOSE_DT'])
            target_date = str(datetime.now().date() - timedelta(days=1))
            if propose_date == target_date:
                names = d['PUBL_PROPOSER']
                names = get_other_proposer(names)
                doc = {
                    'id': d['BILL_ID'],
                    'title': d['BILL_NAME'],  # 법안제목
                    'proposer_names': names,  # 대표제안자 외 제안자
                    'proposer_name': d['RST_PROPOSER'],  # 대표제안자
                    'date': d['PROPOSE_DT'],  # 발의 날짜
                    'url': d['DETAIL_LINK'],  # 상세내용 크롤링 link
                }

                law_list.append(doc)
            else:
                flag = False
                break

    return jsonify(law_list)


def get_allow_mail_list():
    allow_users = list(bp.users.find({'allow_mail':True},{'_id':0, 'username':1}))
    print(allow_users)
    return allow_users


# 매일 오전 9시
cron = "00 09 * * *"

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(get_laws, CronTrigger.from_crontab(cron))
scheduler.start()

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
