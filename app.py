#!/usr/bin/env python

import os, re, json, subprocess, urllib.parse, glob,datetime,csv
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
#from database import *
import logging
from logging import Formatter, FileHandler

# import modules
from modules.email import *
from modules.streaming import *
from util import time_funcs, parse_json

# flask app and db settings
# TODO: settings should be read from encrypted file in production
app = Flask(__name__)
app.secret_key = 'not_for_production'
# app.json_encoder = parse_json.CustomJSONEncoder
# db = loadSession()

def init_app():
    """ Runs prior to app launching, contains initialization code """

    # set logging level
    if settings.ENV == 'DEV':
        logging.basicConfig(level=logging.DEBUG)
    elif settings.ENV == 'TEST':
        logging.basicConfig(level=logging.WARNING)
    elif settings.ENV == 'PROD':
        logging.basicConfig(level=logging.ERROR)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods=['POST'])
def email():
    # send an email
    data = request.json
    dt = datetime.now()
    recipients = []
    recipients.append(data['email'])
    text_body = "This email was sent automatically by Detroit Black Tech system @ << {} >>".format(dt)

    try:
        # DEBUG
        for key, value in data.items():
            print(key,value)

        send_email(recipients=recipients, text_body=text_body, data=data)
        send_stream(data=data, dt=dt)

        return jsonify(
            status=200,
            message='Email delivery success'
        )

    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    init_app()
    #app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=('/root/detroitpbxgui/certs/detroitpbx.com_combined.crt','/root/detroitpbxgui/certs/detroitpbx.com.key'))
    app.run(host='0.0.0.0', port=80, debug=True)
