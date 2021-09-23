from flask import Flask, jsonify, render_template
import requests
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




if __name__ == '__main__':
    app.run()
