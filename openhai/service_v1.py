#!/usr/local/bin/python3
# coding: utf-8
# author: Clement Onawole
# service_v1.py

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
