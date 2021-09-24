import re

from flask import Flask, jsonify, request, Blueprint
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.todaylaw

import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text

bp = Blueprint('crawl', __name__, url_prefix='/')

@bp.route('/api/laws/details', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    id_receive = request.form['id_give']
    title = request.form['title_give']
    # print(url_receive)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (HTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    #title = soup.select_one('body > div > div.contentWrap > div.subContents > h3').text
    proposer= soup.select_one('body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(3)').text
    content = soup.select_one('#summaryContentDiv').text
    date = soup.select_one('body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(2)').text


    count = db.ranking.find_one({'id': id_receive}, {'_id': 0, 'title': 0, 'id': 0})
    if count is not None:
        count = count['count']
        new_count = count + 1
        db.ranking.update_one({'id': id_receive}, {'$set': {'count': new_count}})
    else:
        doc = {
            'id': id_receive,
            'title': title,
            'count': 1
        }
        db.ranking.insert_one(doc)

    return jsonify({'content': content, 'title':title, 'date':date, 'proposer':proposer})

def clean_text(text):
    content = text.get_text()
    cleaned_text = re.sub('[a-zA-Z]', '', content)
    return cleaned_text