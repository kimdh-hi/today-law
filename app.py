from flask import Flask, render_template
import search, app, crawl

app = Flask(__name__)

app.register_blueprint(search.bp) # 법안 조회 API
app.register_blueprint(crawl.bp) # 법안 상세페이지 크롤링 API

@app.route('/')
def index():
    return render_template('index.html')