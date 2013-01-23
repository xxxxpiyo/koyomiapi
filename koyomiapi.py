# -*- coding: utf-8 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hasegawa"
__date__ ="$2013/01/23 17:43:08$"

from flask import Flask

app = Flask(__name__)

@app.route("/koyomi/24sekki", methods=["GET"])
def sekki24():
    return 'aho'

if __name__ == "__main__":
  app.run()