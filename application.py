from flask import Flask, render_template, jsonify
import search, crawl, rank, like, bookmark, category, wish
from login import naver, kakao, google
from urllib import parse
import category_data_scheduler
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from flask_cors import CORS
from decouple import config
from flask_mail import Mail, Message
from pymongo import MongoClient

host = config('MONGO_DB_CLIENT')
client = MongoClient(host, 27017)
db = client.todaylaw

application = Flask(__name__)
api_key = config('API_KEY')
cors = CORS(application, resources={r"/*": {"origins": "*"}})

application.register_blueprint(search.bp) # 법안 조회 API
application.register_blueprint(crawl.bp) # 법안 상세페이지 크롤링 API
application.register_blueprint(rank.bp) # 순위
application.register_blueprint(like.bp) # 좋아요
application.register_blueprint(bookmark.bp) # 즐겨찾기
application.register_blueprint(category.bp) # 카테고리별 조회 API
application.register_blueprint(wish.bp) # 청원

application.register_blueprint(kakao.bp) # 카카오 로그인 API
application.register_blueprint(google.bp) # 구글 로그인 API
application.register_blueprint(naver.bp)

application.register_blueprint(category_data_scheduler.bp)

application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465 # SMTP-TLS 포트
application.config['MAIL_USERNAME'] = config('SENDER_MAIL_ID')
application.config['MAIL_PASSWORD'] = config('SENDER_MAIL_PASSWORD')
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True

mail = Mail(application)

@application.route('/')
def index():
    #return render_template('index.html')
    return 'index'

@application.route('/mail-test')
def mail_send():
    laws = get_laws()
    if len(laws) == 0:
        return jsonify({"success":False,"msg":"어제 발의된 법안이 없습니다."})
    user_mail_list = get_allow_mail_list()

    recipients = []
    for user_mail in user_mail_list:
        recipients.append(user_mail['username'])
    print('수신 리스트 : ', recipients)
    msg = Message("[오늘의 국회] - 어제자 발의법률안 알림 메시지", sender=application.config['MAIL_USERNAME'], recipients=recipients)

    title = "<div style='width:100%; margin:auto; text-align:center'><h1>어제자 발의 법률안</h1></div>"
    table_head = "<thead style='font-size:20px; text-align:center;'><tr style='padding: 10px; border: 1px solid black;'><td style='padding: 10px; border: 1px solid black;'>제목</td><td style='padding: 10px; border: 1px solid black;'>대표발의자</td><td style='padding: 10px; border: 1px solid black;'>상세정보 링크</td></tr></thead>"
    table_row = ""

    for law in laws:
        print(law['title'], law['proposer_name'], law['url'])
        table_row += f"<tr style='padding: 10px; border: 1px solid black;'><td style='padding: 10px; border: 1px solid black;'>{law['title']}</td><td style='padding: 10px; border: 1px solid black; text-align: center;'>{law['proposer_name']}</td><td style='padding: 10px; border: 1px solid black; text-align: center;'><a href='{law['url']}'>상세정보</a></td></tr>"

    html_template = f"{title}<table style='width: 100%; border: 3px solid black; border-collapse: collapse;'>{table_head}<tbody>{table_row}</tbody></table>"
    msg.html = html_template

    mail.send(msg)

    return jsonify({"success":True,"msg":"알림 메일 발송이 완료되었습니다."})

# 발의된 날짜가 어제인 법안을 받아온다.
def get_laws():
    age = 21
    type = 'json'
    flag = True
    pIndex = 0
    law_list = []
    while flag:
        pIndex+=1
        url = f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={api_key}&Type={type}&AGE={age}&pIndex={pIndex}&pSize=10'
        data = requests.get(url).json()
        data = data['nzmimeepazxkubdpn'][1]['row']

        for d in data:
            propose_date = str(d['PROPOSE_DT'])
            target_date = str(datetime.now().date() - timedelta(days=1))
            if propose_date >= target_date:
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

    return law_list

# users DB에서 알람 메일을 받기로 한 사용자의 정보를 가져온다. (receive_mail is True)
def get_allow_mail_list():
    allow_users = list(db.users.find({'receive_mail':True},{'_id':0, 'username':1}))
    return allow_users


# 화요일~토요일 매일 오전 9시
cron = "52 12 * * 0"
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(mail_send, CronTrigger.from_crontab(cron))
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

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
