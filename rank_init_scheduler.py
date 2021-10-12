import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Blueprint
from pymongo import MongoClient

MONGO_URL = os.environ['MONGO_URL']
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
client = MongoClient(MONGO_URL, 27017, MONGO_USERNAME, MONGO_PASSWORD)
db = client.todaylaw

bp = Blueprint("rank_init_scheduler", __name__, url_prefix="/")

@bp.route('/rank/data')
def init_ranking_collection():
    print("조회수 순위 DB 초기화 시작")
    result = db.ranking.delete_many({})
    print(f"조회수 순위 DB 초기화 종료 {result.deleted_count}건 삭제")
    return "ok"

# 매달 매주 월요일 오전 3시 정각
cron = "00 03 * * mon"

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(init_ranking_collection, CronTrigger.from_crontab(cron))
scheduler.start()