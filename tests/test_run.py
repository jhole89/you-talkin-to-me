from app.run import *
import json


def test_app():

    assert app is not None
    assert type(app) == Flask


def test_chatbot():

    assert chatbot.name == 'Arnold Schwartzenatter'


def test_home(client):
    req = client.get('/')

    assert req.status_code == 200
    assert list(req.headers) == [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', '1273')]


def test_get_raw_response(client):
    req = client.get('/question/who%20are%20you')

    assert req.status_code == 200
    assert req.data == b'Arnold Schwartzenatter'


def test_retrain_corpus(client):

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'conversation_length': 5,
        'stop_short': 10
    }

    req = client.post('/admin/retrain', data=json.dumps(data), headers=headers)

    assert req.status_code == 200
    assert req.data == str.encode('Retrained with parameters: {}'.format(data))
