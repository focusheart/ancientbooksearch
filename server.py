# -*- coding: utf8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, send_from_directory, \
     jsonify, Response
from elasticsearch import Elasticsearch
import logging
import logging.config

# site config 
DEBUG = True
HOST = '0.0.0.0'
PORT = 50407
ES_HOST = 'localhost'
ES_INDEX = 'ancientbooks'
ES_DOCTYPE = 'book'

# config logging
logging.config.fileConfig('logger.conf')
logger = logging.getLogger('root')

# config es
es = Elasticsearch(ES_HOST)

# create the app
app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/q', methods=['GET','POST'])
def q():
    k = request.form.get('k')
    s = request.form.get('s')
    f = request.form.get('f')
    if k is None or k=='': return jsonify({'success':False})
    if s is None or s=='': s = 7
    else:                  s = int(s)
    if f is None or f=='': f = 0
    else:                  f = int(f)
    
    # construct a search body
    body = {
        "query": {
            "multi_match": {
                "query": k,
                "fields": ['title','info']
            }
        },
        "highlight": {
            "fields": {
                "title": {},
                "info" : {}
            }
        }
    }
    # Start use ES!
    recs = es.search(index=ES_INDEX, from_=f*s, \
        doc_type=ES_DOCTYPE, size=s, body=body)

    # Pagination
    tt = recs['hits']['total']
    if tt%s==0: np = tt/s
    else:       np = tt/s + 1
    
    # return package
    ret = {'success':True, 'pager':{'tt':tt,'np':np,'pn':f}, \
        "hits":recs['hits']['hits']}

    return jsonify(ret)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
