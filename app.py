import re

from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/test')
def test():
    type = 'json'
    age = '21'
    res = requests.get(f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}')
    print(res.json())
    return jsonify(res.json())

@app.route('/api/laws/details', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    # print(url_receive)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (HTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('body > div > div.contentWrap > div.subContents > h3').text
    proposer= soup.select_one('body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(3)').text
    content = soup.select_one('#summaryContentDiv').text
    date = soup.select_one('body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(2)').text

    print(title)

    return jsonify({'content': content, 'title':title, 'date':date, 'proposer':proposer})

def clean_text(text):
    content = text.get_text()
    cleaned_text = re.sub('[a-zA-Z]', '', content)
    return cleaned_text

if __name__ == '__main__':
    app.run()
