from flask import Flask, render_template
import search, crawl, rank, like, bookmark, category
from login import kakao, google
import category_data_scheduler, rank_init_scheduler

app = Flask(__name__)

app.register_blueprint(search.bp) # 법안 조회 API
app.register_blueprint(crawl.bp) # 법안 상세페이지 크롤링 API
app.register_blueprint(rank.bp) # 순위
app.register_blueprint(like.bp) # 좋아요
app.register_blueprint(bookmark.bp) # 즐겨찾기
app.register_blueprint(category.bp) # 카테고리별 조회 API

app.register_blueprint(kakao.bp) # 카카오 로그인 API
app.register_blueprint(google.bp) # 구글 로그인 API

app.register_blueprint(category_data_scheduler.bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)