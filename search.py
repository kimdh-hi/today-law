import base64

from flask import Flask, jsonify, request, Blueprint
import requests
from urllib import parse
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text

bp = Blueprint('search', __name__, url_prefix='/')

# open api 주소
# https://open.assembly.go.kr/portal/data/service/selectServicePage.do/OK7XM1000938DS17215

type = 'json'
age = '21'

##=========================================##
# 법안명, 발의제안자로 발의법안 조회 API
# 1. 검색조건(condition)이 없는 경우 그냥 조회
# 2. 검색조건이 법안명인 경우 법안명(BILL_NAME)으로 조회
# 3. 검색조건이 제안자명인 경우 제안자명(PROPOSER)로 조회
##=========================================##
@bp.route('/api/laws')
def get_laws():
    query = request.args.get('query')
    proposer_name = request.args.get('proposer')
    condition = request.args.get('condition')
    pIndex = request.args.get('offset')

    #== 검색조건이 없는 경우 ==#
    if query is None and condition is None:
        data = requests.get(
            f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}&pIndex={pIndex}&pSize=10')
    #== 법안명으로 검색 ==#
    elif condition == '법안명':
        url = f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}&BILL_NAME={query}&pIndex={pIndex}&pSize=10'
        query = encode_querystring(url)

        data = requests.get('https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?' + query)
    #== 법안발의 제안자명으로 검색==#
    # http://localhost:5000/api/laws?offset=1&proposer=%EA%B9%80%EA%B4%91%EB%A6%BC&condition=%EC%A0%9C%EC%95%88%EC%9E%90
    elif condition == '제안자':
        url = f'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?Key={apiKey}&Type={type}&AGE={age}&PROPOSER={proposer_name}&pIndex={pIndex}&pSize=10'
        query = encode_querystring(url)

        data = requests.get('https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?' + query)

    data = data.json()
    total_count = data['nzmimeepazxkubdpn'][0]['head'][0]['list_total_count']
    data = data['nzmimeepazxkubdpn'][1]['row']

    response = []
    response.append({'total_count':total_count})
    for d in data:
        names = d['PUBL_PROPOSER']
        names = get_other_proposer(names)

        response.append({
            'id':d['BILL_ID'],
            'title':d['BILL_NAME'],               # 법안제목
            'proposer_name':d['RST_PROPOSER'],    # 대표제안자
            'proposer_names':names,               # 대표제안자 외 제안자
            'date':d['PROPOSE_DT'],               # 발의 날짜
            'url':d['DETAIL_LINK'],               # 상세내용 크롤링 link
        })

    return jsonify(response)

# 요청 URL에서 문자열 쿼리스트링 인코딩
def encode_querystring(url):
    url = parse.urlparse(url)
    query = parse.parse_qs(url.query)
    query = parse.urlencode(query, doseq=True)

    return query

def get_other_proposer(names):
    names = names.split(',')
    names_len = len(names)
    names = ','.join(names[:10])
    if names_len > 10:
        extra = names_len - 10
        names = names + f' 외 {extra}명'
    return names