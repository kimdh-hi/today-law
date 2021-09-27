from flask import Flask, render_template
import search, app, crawl, rank, like, bookmark

app = Flask(__name__)

app.register_blueprint(search.bp) # 법안 조회 API
app.register_blueprint(crawl.bp) # 법안 상세페이지 크롤링 API
app.register_blueprint(rank.bp) # 순위
app.register_blueprint(like.bp) # 좋아요
app.register_blueprint(bookmark.bp) # 즐겨찾기

@app.route('/')
def index():
    return render_template('index.html')