from flask import Flask, render_template
import search, app

app = Flask(__name__)

app.register_blueprint(search.bp)

@app.route('/')
def index():
    return render_template('index.html')