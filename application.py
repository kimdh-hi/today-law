from flask import Flask, render_template
import search, crawl, rank, like, bookmark, category, wish, mail
from login import naver, kakao, google
import category_data_scheduler, rank_init_scheduler
from flask_cors import CORS
from flask_mail import Mail, Message

application = Flask(__name__)
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

application.register_blueprint(mail.bp)

application.register_blueprint(category_data_scheduler.bp)

application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'zbeld123@gmail.com'
application.config['MAIL_PASSWORD'] = '@@kimd6704'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True

mail = Mail(application)

@application.route('/')
def index():
    msg = Message("test mail", sender='zbeld123@gmail.com', recipients=["zbeld123@naver.com"])
    msg.html = '<h1>TEST</h1>'

    mail.send(msg)

    return render_template('index.html')

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
