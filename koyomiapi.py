# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hasegawa"
__date__ ="$2013/01/23 17:43:08$"

from flask import Flask, request, g
import datetime

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
    
    # no
    try:
        for i in request.args["index"].split(","):
            index.append(int(i))
    
    except ValueError:
        return invalidParameter()
    except:
        pass
    
    return "date:{0}/{1}/{2} {3}:{4} year={5}".format(g.date.year, g.date.month,g.date.day, g.date.hour, g.date.minute,str(year))
        



def invalidParameter(code=400):
    return "Invalid parameter", code

if __name__ == "__main__":
    app.debug = True
    app.run()