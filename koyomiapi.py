# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hasegawa"
__date__ ="$2013/01/23 17:43:08$"

from flask import Flask, request, g, json
import datetime
import sys


#sys.path.append("/Users/hasegawa/NetBeansProjects/koyomi/koyomi")

from sekki24 import get24SekkiDay

app = Flask(__name__)

@app.before_request
def getToday():
    g.date = datetime.datetime.today()

@app.route("/24sekki", methods=["GET"])
def sekki24():
    
    year = g.date.year
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
    
    #return "dyear={0} index={1}".format(str(year),str(index))
    #return str(get24SekkiJSON(year,index)).decode("utf-8")
    s = u'あほ'
    return json.dumps(get24SekkiJSON(year,index))
        

def get24SekkiJSON(year, index):
    result = get24SekkiDay(year,index) if len(index) > 0 else get24SekkiDay(year)
    result2 = []
    for i in result:
        i["name"] = i["name"].encode("utf-8")
        result2.append(i)
    return result
    


def invalidParameter(code=400):
    return "Invalid parameter", code

if __name__ == "__main__":
    app.debug = True
    app.run()