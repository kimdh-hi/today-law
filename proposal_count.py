from flask import request, Blueprint
import requests
from urllib import parse
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
apiKey = tree.find('string[@name="api-key"]').text

bp = Blueprint('proposal_count', __name__, url_prefix='/')

type = 'json'
age = '21'

@bp.route('/total-count', methods=['GET'])
def get_proposal_count():
    pass

def encode_querystring(url):
    url = parse.urlparse(url)
    query = parse.parse_qs(url.query)
    query = parse.urlencode(query, doseq=True)

    return query
