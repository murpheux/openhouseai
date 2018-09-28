#!/usr/local/bin/python3
# coding: utf-8
# author: Clement Onawole
# test_service.py

import pytest
import json
from .service_v1 import create_app
from flask import url_for, testing
from flask.testing import FlaskClient


@pytest.fixture
def app():
    data = """lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy
            eirmod tempor invidunt ut labore et dolore magna aliquyam erat sed diam
            voluptua at vero eos et accusam et justo duo dolores et ea rebum stet clita
            kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem
            ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod"""
            
    data = data.splitlines()

    app = create_app(data)
    app.debug = True
    return app


def test_service_availability(client):
    res = client.get(url_for('index'))
    assert res.status_code == 200
    assert res.json == {'Service': 'app indexer api service v1 (c) 2018 1.0 0.0.0'}


def test_search_get_with_no_argument(client):
    res = client.get(url_for('search'))
    assert res.status_code == 200
    assert res.json == {}


def test_search_get_with_argument_no_known_argument(client):
    res = client.get(url_for('search', btree=''))
    assert res.status_code == 200
    assert res.json == {}
    

def test_search_get_with_argument_blank(client):
    res = client.get(url_for('search', search=''))
    assert res.status_code == 200
    assert res.json == {}


def test_search_get_with_argument_not_found(client):
    res = client.get(url_for('search', search='medusa'))
    assert res.status_code == 200
    assert res.json == {'number_of_occurrences': 0, 'occurrences': [], 'query_text': 'medusa'}


def test_search_get_with_argument_value_found_one(client):
    res = client.get(url_for('search', search='duo'))
    assert res.status_code == 200
    assert res.json == {'number_of_occurrences': 1,
                        'occurrences': [{'end': 56,
                                         'in_sentence': '            voluptua at vero eos et accusam '
                                         'et justo duo dolores et ea rebum stet clita',
                                         'line': 3,
                                         'start': 53}],
                        'query_text': 'duo'}


def test_search_get_with_argument_value_found_n(client):
    res = client.get(url_for('search', search='lorem'))
    assert res.status_code == 200
    assert res.json == {'number_of_occurrences': 3, 'occurrences': [{'end': 5, 'in_sentence': 'lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy', 'line': 1, 'start': 0}, {
        'end': 60, 'in_sentence': '            kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem', 'line': 4, 'start': 55}, {'end': 87, 'in_sentence': '            kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem', 'line': 4, 'start': 82}], 'query_text': 'lorem'}


# post reqquires a valid json
def test_search_post_with_argument_no_known_argument(client):
    res = client.post(url_for('search'), data=json.dumps(dict(btree='')), content_type='application/json')
    assert res.status_code == 200
    assert res.json == {}


def test_search_post_with_argument_blank(client):
    res = client.post(url_for('search'), data=json.dumps(dict(search='')), content_type='application/json')
    assert res.status_code == 200
    assert res.json == {}


def test_search_post_with_argument_not_found(client):
    res = client.post(url_for('search'), data=json.dumps(dict(search='medusa')), content_type='application/json')
    assert res.status_code == 200
    assert res.json == {'number_of_occurrences': 0, 'occurrences': [], 'query_text': 'medusa'}


def test_search_post_with_argument_value_found_one(client):
    res = client.post(url_for('search'), data=json.dumps(dict(search='duo')), content_type='application/json')
    assert res.status_code == 200
    assert res.json == {'number_of_occurrences': 1,
                        'occurrences': [{'end': 56,
                                         'in_sentence': '            voluptua at vero eos et accusam '
                                         'et justo duo dolores et ea rebum stet clita',
                                         'line': 3,
                                         'start': 53}],
                        'query_text': 'duo'}


def test_search_post_with_argument_value_found_n(client):
    res = client.post(url_for('search'), data=json.dumps(dict(search='lorem')), content_type='application/json')
    assert res.status_code == 200
    assert res.json == {'number_of_occurrences': 3, 'occurrences': [{'end': 5, 'in_sentence': 'lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy', 'line': 1, 'start': 0}, {
        'end': 60, 'in_sentence': '            kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem', 'line': 4, 'start': 55}, {'end': 87, 'in_sentence': '            kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem', 'line': 4, 'start': 82}], 'query_text': 'lorem'}
