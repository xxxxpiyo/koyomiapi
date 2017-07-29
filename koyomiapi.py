# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hasegawa"
__date__ ="$2013/01/23 17:43:08$"

from flask import Flask, request, g, json, make_response
import datetime
import sys
import dict2xml

sys.path.append("/Users/hasegawa/git/koyomi")

from sekki24 import get24SekkiDay

app = Flask(__name__)

@app.before_request
def getToday():
    g.date = datetime.datetime.today()

@app.route("/24sekki.json", methods=["GET"])
def sekki24_json():
    resp = make_response(json.dumps(get_sekki24(request)))
    resp.headers['Content-type'] = "application/json; charset: UTF-8"
    return resp

@app.route("/24sekki.jsonp", methods=["GET"])
def sekki24_jsonp():
    try:
        callback=request.args["callback"]
    except:
        callback="callback"
    
    resp = make_response(callback+"(" + json.dumps(get_sekki24(request)) + ")")
    resp.headers['Content-type'] = "application/javascript; charset: UTF-8"
    return resp
    
@app.route("/24sekki", methods=["GET"])
@app.route("/24sekki.xml", methods=["GET"])
def sekki24_xml():
    resp = make_response(dict2xml.dict2xml(get_sekki24(request)))
    resp.headers['Content-type'] = "text/xml; charset: UTF-8"
    return resp

def get_sekki24(request):
    
    year = g.date.year
    month = None
    index = []
    
    #
    # 引数チェック
    #
    
    # year
    try:
        year = int(request.args["year"])
    
    except ValueError:
        return invalidParameter()
    except:
        pass

    # month
    try:
        month = int(request.args["month"])

    except ValueError:
        return invalidParameter()

    except :
        month = None

    # このAPIは1901 - 2099までしか対応していない
    if year < 1901 or year > 2099:
        return invalidParameter()
    
    # index
    try:
        for i in request.args["index"].split(","):
            
            # 1 - 24まで
            if int(i) < 1 or 24 < int(i):
                return invalidParameter()
            
            index.append(int(i))
    
    except ValueError:
        return invalidParameter()
    except:
        pass
    
    # indexがある場合、重複を除外
    if len(index) > 0:
        index = list(set(index))
    
    return get24SekkiDay(year,month,index) if len(index) > 0 else get24SekkiDay(year,month)

def invalidParameter(code=400):
    return "Invalid parameter", code

if __name__ == "__main__":
    app.debug = True
    app.run()