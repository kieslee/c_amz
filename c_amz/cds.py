#-*- coding: UTF-8 -*-

import socket
import struct
import math
import sys
import traceback
import json
import flask
from flask import Flask
from flask import request
app = Flask(__name__)

from acache import r_push, list_len

from conf import crawls
crawls_num = len(crawls)
crawls_index = 0

max_cap = 5000000


def make_response(data=None, code=200, headers=None, raw=False):
    if data is None:
        data = True
    h = {
        'Cache-Control': 'no-cache',
        'Expires': '-1',
        #'Content-Type': 'application/json'
        'Content-Type': 'text/plain'
    }
    if headers:
        h.update(headers)

    if h['Cache-Control'] == 'no-cache':
        h['Pragma'] = 'no-cache'

    try:
        if raw is False:
            data = json.dumps(data, sort_keys=True, skipkeys=True)
    except TypeError:
        data = str(data)
    return flask.current_app.make_response((data, code, h))


def valid_format(c):
    if c.has_key('num') is False:
        return False

    if c.has_key('commands') is False:
        return False

    if type(c['commands']) != type([]):
        return False

    for item in c['commands']:
        if item.has_key('uuid') is False:
            return False

    return True


def judge_cap(input_num):
    sum = 0
    for c in crawls:
        sum += list_len(c)

    if (input_num + sum) > (max_cap * crawls_num):
        return False

    return True


@app.route('/', methods=['POST'])
def get_command():
    global crawls_index
    command_list = request.json
    if valid_format(command_list) is False:
        return make_response({'msg': 'command format invalid'}, code=400)

    if judge_cap(command_list['num']) is False:
        return make_response({'msg': 'max capacity overflow'}, code=400)

    for c in command_list['commands']:
        print c
        try:
            r_push(crawls[crawls_index], json.dumps(c))
            crawls_index += 1
            if crawls_index >= crawls_num:
                crawls_index = 0
        except Exception, e:
            traceback.print_exc(e)
            return make_response({'msg': 'put command into queue failed'}, code=400)

    return make_response({'msg': 'OK'}, code=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
