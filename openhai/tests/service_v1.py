#!/usr/local/bin/python3
# coding: utf-8
# author: Clement Onawole
# service_v1.py

import flask
from flask import Flask, jsonify, json
import re

app_name = "app indexer api service v1 (c) 2018"
version = "1.0"
build = "0.0.0"


def create_app(data=None):
    app = Flask(__name__)

    if not data:
        with open('data/king-i.txt', 'r') as file:
            data = file.readlines()

    def search_in_data(search_string):
        line = 0

        for st in data:
            line = line + 1
            for m in re.finditer(search_string, st):
                yield line, m.start(), m.end(), st


    def replace_quote_in_string_and_newline(val):
        val = val.replace('"', '~')
        val = val.replace("'", '~')
        val = val.replace('\n', '')

        return val

    def construct_json(search_string, result):
        mlen = 0

        injson = ''
        for x in result:
            mlen += 1
            injson += '{'
            injson += f'"line" :  {x[0]}, '
            injson += f'"start" :  {x[1]}, '
            injson += f'"end" :  {x[2]}, '
            injson += f'"in_sentence" :  "{replace_quote_in_string_and_newline(x[3])}"'
            injson += '}, '

        injson = injson[:-2]  # remove last comma
        mjson = '{'
        mjson += f'"query_text" : "{search_string}", '
        mjson += f'"number_of_occurrences" : {mlen}, '

        mjson += f'"occurrences" : [ {injson} ]'
        mjson += '}'

        return mjson


    # service 1
    @app.route('/api')
    def index():
        return jsonify({"Service": f"{app_name} {version} {build}"})


    # service 2
    @app.route('/api/search', methods=['GET', 'POST'])
    def search():
        search_string = None

        if flask.request.method == 'POST':
            #search = flask.request.values.get('search')
            body = flask.request.get_json()

            if 'search' in body:
                search_string = str(body['search'])
        else:
            search_string = flask.request.args.get('search')

        if not search_string:
            return jsonify({})
        else:
            result = search_in_data(search_string)
            js = construct_json(search_string, result)

            return jsonify(json.loads(js))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
