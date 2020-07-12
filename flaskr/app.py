from flask import Flask,request,jsonify,render_template,redirect,url_for
from hash import base62_encode,base62_decode
from flaskr.db import get_db
import requests
import json
from datetime import datetime
from markupsafe import escape

app = Flask(__name__)
short_to_long = {}
index = 1
records = []
@app.route('/',methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        global index
        url = request.form['url']
        token = base62_encode(index)
        short_url = 'http://127.0.0.1:5000/{}'.format(token)
        short_to_long[short_url] = url
        """
        index = get_max_index()
        print (index)
        token = base62_encode(index)
        short_url = 'http://127.0.0.1:8002/{}'.format(token)
        save_url(short_url, url)
        """
        return redirect(url_for("track",token=token))

    return render_template('index.html')

@app.route('/track/<token>')
def track(token):
    print(token)
    print(short_to_long)
    short_url = 'http://127.0.0.1:5000/{}'.format(token)

    #檢查有無紀錄
    if short_url in short_to_long:
        trace_code = token
        trace_url = 'http://127.0.0.1:5000/track/{}'.format(trace_code)
        long_url = short_to_long[short_url]
        

    return render_template('track.html', **locals(),records=records)


@app.route('/<token>')
def redirect_url(token):
    print(token)
    short_url = 'http://127.0.0.1:5000/{}'.format(token)
    if short_url in short_to_long:
        return redirect(short_to_long[short_url], code=302)
    
    ##save record to db
    record = {}
    record["short_url"] =  short_url
    record["datetime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record["ip"] = request.environ.get('REMOTE_ADDR')
    record["port"] = request.environ.get('REMOTE_PORT')
    record["user_agent"] = request.environ.get('HTTP_USER_AGENT')
    records.append(record)
    return jsonify({'short_url':short_url})

@app.route("/get_client_info", methods=["GET"])
def get_client_information():
    """
    bulk
    http://api.ipstack.com/134.201.250.155,72.229.28.185,110.174.165.78
    ? access_key = YOUR_ACCESS_KEY
    """

    #ipstack_api_key = "427408a7bcbc99d0410bcd2e9fd8e004"
    #url =  "http://api.ipstack.com/{}?access_key={}".format(request.remote_addr,ipstack_api_key)
    #response = requests.get(url)
    #info = json.loads(response.text)
    info = {}
    info["port"] = request.environ.get('REMOTE_PORT')
    if 'HTTP_X_REAL_IP' in request.environ:
        ip = request.environ.get('HTTP_X_REAL_IP')
    elif 'CF-Connecting-IP' in request.headers:
        ip = request.headers['CF-Connecting-IP']
    elif request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.environ.get('REMOTE_ADDR')

    info["ip"] = ip
    return jsonify(info), 200
  
def get_max_index():
    db = get_db()
    max_index = db.execute(
        'SELECT max(id) in url'
    ).fetchone()
    return max_index

def save_url(short_url, long_url):
    db = get_db()
    db.execute(
        'INSERT INTO url (short_url, long_url)'
        ' VALUES (?, ?, ?)',
        (short_url, long_url)
    )
    db.commit()
    return 
