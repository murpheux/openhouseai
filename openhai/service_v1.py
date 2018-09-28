#!/usr/local/bin/python3
# coding: utf-8
# author: Clement Onawole
# service_v1.py

import flask
import re
import connexion
from flask import Flask, jsonify, json

app_name = "app indexer api service v1 (c) 2018"
version = "1.0"
build = "0.0.0"


def create_app(data=[]):
    app = Flask(__name__)
    #app = connexion.FlaskApp(__name__, specification_dir='./')
    #app.add_api('swagger.yml')


    def search_in_data(search_string):
        line = 0

        if not data:
            with open('data/king-i.txt', 'r') as file:
                for text_line in file:
                    data.append(text_line)
                    line = line + 1
                    for m in re.finditer(search_string, text_line):
                        yield line, m.start(), m.end(), text_line
        else:
            for text_line in data:
                line = line + 1
                for m in re.finditer(search_string, text_line):
                    yield line, m.start(), m.end(), text_line

    def replace_quote_in_string_and_newline(val):
        val = val.replace('"', '~')
        val = val.replace("'", '~')
        val = val.replace('\n', '')

        return val

    def construct_json(search_string, result):
        length = 0

        injson = ''
        for res in result:
            length += 1
            injson += '{'
            injson += f'"line" :  {res[0]}, '
            injson += f'"start" :  {res[1]}, '
            injson += f'"end" :  {res[2]}, '
            injson += f'"in_sentence" :  "{replace_quote_in_string_and_newline(res[3])}"'
            injson += '}, '

        injson = injson[:-2]  # remove last comma
        mjson = '{'
        mjson += f'"query_text" : "{search_string}", '
        mjson += f'"number_of_occurrences" : {length}, '

        mjson += f'"occurrences" : [ {injson} ]'
        mjson += '}'

        return mjson


    @app.route('/api')
    def index():
        """
        service introduction/ping

        :return: json
        """
        return jsonify({"Service": f"{app_name} {version} {build}"})


    @app.route('/api/search', methods=['GET', 'POST'])
    def search():
        """
        main search/index service

        :return: json
        """
        search_string = None

        if flask.request.method == 'POST':
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


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
