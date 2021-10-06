import os
import pathlib

import requests
import google.auth.transport.requests
from flask import Blueprint, Flask, session, abort, redirect, request, render_template, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.todaylaw

bp = Blueprint("google", __name__, url_prefix='/')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# key 관리
from decouple import config

GOOGLE_CLIENT_ID = config('Google_API')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper


@bp.route("/login_google")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    find_user = db.users.find_one({'id': id_info['sub']})
    if find_user == None:
        user_info_doc = {
            "id": id_info.get("sub"),
            "username": id_info.get("email"),
            "name": id_info.get("name"),
            "profile_image": id_info.get("picture"),
            "like_laws": [],
            "hate_laws": [],
            "bookmarks": []
        }

        db.users.insert_one(user_info_doc)

    return redirect("/protected_area")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/protected_area")
@login_is_required
def protected_area():
    print("login ok!")
    return redirect("/")
