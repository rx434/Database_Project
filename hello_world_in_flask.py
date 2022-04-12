# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:06:00 2020

@author: xinfe
"""

from flask import Flask, render_template
import pymysql.cursors

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello_world.html')

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)