from flask import redirect, request, jsonify, Blueprint
import requests
from decouple import config

bp = Blueprint("kakao_login", __name__, url_prefix='/')

kakao_client_key = config('KAKAO_REST_API')
redirect_uri = "http://localhost:5000/oauth/kakao/callback"

# 사용자가 카카오 로그인 요청시 카카오 로그인 페이지로 이동
# 사용자가 카카오에 인증 성공시 지정한 Redirect_URI로 Access_token을 요청할 수 있는 인증토큰(Authentication_code)를 응답받는다.
@bp.route('/oauth/kakao')
def redirect_kakao_login_page():
    kakao_redirect_url = f"https://kauth.kakao.com/oauth/authorize?client_id={kakao_client_key}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_redirect_url)

# 인증토큰을 응답받고 응답받은 인증토큰으로 Access_token을 요청한 후 응답받은 Access_token으로 사용자 정보를 요청
@bp.route('/oauth/kakao/callback')
def access():
    code = request.args.get('code')
    access_token_request_url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={kakao_client_key}&redirect_uri={redirect_uri}&code={code}"
    response_token = requests.get(access_token_request_url).json()
    token = response_token['access_token']

    user_info_request_url="https://kapi.kakao.com/v2/user/me"
    user_info = requests.get(user_info_request_url, headers={"Authorization":f"Bearer {token}"})

    login(user_info)

    return jsonify(user_info.json())

def login(user):
    print(user)

    return "login ok"


