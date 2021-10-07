from flask import Blueprint
import requests
from urllib import parse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text

from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.todaylaw

bp = Blueprint("category_data_scheduler", __name__, url_prefix='/')

age = 21
type = 'json'

g_categories = [
    {"건설":["건설"]},
    {"노동/근로":["노동", "근로"]}, # 노동/근로 카테고리 클릭시 [노동, 근로]가 검색되도록 처리
    {"문화":["문화"]},
    {"부동산":["범죄"]},
    {"의료/보건":["의료","보건"]},
    {"보험":["보험"]},
    {"주택":["주택"]},
    {"조세":["조세"]},
    {"교육":["교육"]},
    {"선거":["선거"]},
    {"농수산물":["농산물","수산물"]}, # 농수산물 카테고리 검색시 [농산물, 수산물]이 검색되도록 처리
    {"병역":["병역"]},
    {"범죄":["범죄"]},
    {"금융":["금융", "은행"]},
    {"정보통신":["정보통신", "정보보호"]},
]

# 카테고리 데이터 저장 스케줄러 job 메서드
@bp.route('/category/data')
def set_category_data():
    # 카테고리 데이터 DB 데이터 삭제
    db.category.delete_many({})

    for g_category in g_categories:
        for category in g_category:
            print(f"데이터 수집 : {category}")
            detail_categories = g_category[category]
            for keyword in detail_categories:
                url = f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}&BILL_NAME={keyword}&pIndex=1&pSize=50'
                query = encode_querystring(url)
                data = requests.get('https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?' + query)

                data = data.json()
                data = data['nzmimeepazxkubdpn'][1]['row']

                for d in data:
                    now = datetime.now() - timedelta(days=90) # 90일 전
                    target_date = now.strftime('%Y-%m-%d')
                    propose_date = d['PROPOSE_DT']
                    names = d['PUBL_PROPOSER']
                    names = get_other_proposer(names)
                    # 발의날짜가 90일 이내인 것만 DB에 저장
                    if propose_date >= target_date:
                        doc = {
                            'id': d['BILL_ID'],
                            'title': d['BILL_NAME'],  # 법안제목
                            'proposer_names': names,  # 대표제안자 외 제안자
                            'proposer_name': d['RST_PROPOSER'],  # 대표제안자
                            'date': d['PROPOSE_DT'],  # 발의 날짜
                            'url': d['DETAIL_LINK'],  # 상세내용 크롤링 link
                            'category': category,   # 카테고리
                        }
                        db.category.insert_one(doc)
                    else:
                        break
    return "ok"

# 매일 오전 3시
# 00분 03시 매일 매달 매주
cron = "00 03 * * *"

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(set_category_data, CronTrigger.from_crontab(cron))
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