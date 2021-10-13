from flask import render_template, Blueprint

bp = Blueprint('mypage', __name__, url_prefix='/')

@bp.route('/mypage')
def index():
    return render_template('mypage.html')