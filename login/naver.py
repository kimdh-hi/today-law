from urllib.parse import quote

from flask import redirect, request, jsonify, Blueprint, make_response, render_template
import requests
from decouple import config
from pymongo import MongoClient
from datetime import datetime, timedelta
from urllib import parse
import jwt

client = MongoClient('localhost', 27017)
db = client.todaylaw

bp = Blueprint("naver_login", __name__, url_prefix='/')

naver_client_key = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')
jwt_secret = config('JWT_SECRET')
# UTF-8로 URL Encoding
redirect_uri = quote("http://localhost:5000/oauth/naver/callback", encoding='UTF-8')


# 사용자가 네이버 로그인 요청시 네이버 로그인 페이지로 이동
# 사용자가 네이버에 인증 성공시 지정한 Redirect_URI로 Access_token을 요청할 수 있는 인증토큰(Authentication_code)를 응답받는다.
@bp.route('/oauth/naver', methods=["GET"])
def redirect_naver_login_page():
    naver_redirect_url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={naver_client_key}&redirect_uri={redirect_uri}"
    return redirect(naver_redirect_url)


# 인증토큰을 응답받고 응답받은 인증토큰으로 Access_token을 요청한 후 응답받은 Access_token으로 사용자 정보를 요청
@bp.route('/oauth/naver/callback')
def access():
    try:
        code = request.args.get('code')
        # access_token_request_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver_client_key}&redirect_uri={redirect_uri}&code={code}"
        access_token_request_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver_client_key}&client_secret={naver_client_secret}&code={code}"
        response_token = requests.get(access_token_request_url).json()
        token = response_token['access_token']

        user_info_request_url = "https://openapi.naver.com/v1/nid/me"
        user_info_response = requests.get(user_info_request_url, headers={"Authorization": f"Bearer {token}"})
        user_info = user_info_response.json()
        print(user_info)
        # DB에 user 정보를 넣어주고 jwt를 생성해서 쿠키에 넣어서 클라이언트에게 넘겨준다.
        naver_account = user_info['response']
        print(naver_account)

        id = str(naver_account['id'])

        find_user = db.users.find_one({'user_id': id})

        if find_user == None:
            user_info_doc = {
                "user_id": id,
                "username": naver_account['email'],
                "name": naver_account['nickname'],
                "profile_image": naver_account['profile_image'],
                "like_laws": [],
                "hate_laws": [],
                "bookmarks": []
            }

            db.users.insert_one(user_info_doc)
    except:
        return jsonify({"result": "fail"})

    return login(id, naver_account['nickname'])


def login(id, name):
    # JWT 토큰 구성
    payload = {
        "user_id": id,
        "name": name,
        "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        # "exp": datetime.utcnow() + timedelta(seconds=60) # 테스트용으로 10초만 유효한 토큰 생성
    }

    # JWT 토큰 생성
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')

    # 쿠키를 담은 response를 구성하기 위해 make_response 사용
    response = make_response(redirect('/'))
    # 쿠키에 토큰 세팅
    response.set_cookie('mytoken', token)

    return response


# jwt 토큰 + 쿠키 테스트
@bp.route('/login-check')
def login_check():
    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])

        user = db.users.find_one({'user_id': payload['user_id']}, {'_id': False})
        return jsonify({'result': 'success', 'name': user['name']})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/')
