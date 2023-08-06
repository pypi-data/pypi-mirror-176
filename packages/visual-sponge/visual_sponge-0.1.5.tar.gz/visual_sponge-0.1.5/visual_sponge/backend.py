"""
This module starts the backend of the web
"""
import os
import sys
from io import StringIO
import traceback

from flask import Flask, render_template, send_from_directory, request, jsonify
import webbrowser

from . import MACROS, Xponge
from .commands import *


def run():
    app = Flask(MACROS.PACKAGE,
                template_folder=os.path.join(os.path.dirname(__file__), "templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "static"))

    @app.template_filter('localization')
    def localization(key):
        return MACROS.CURRENT_LANGUAGE.get(key, key)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(os.path.dirname(__file__), "static"),
                                   path='favicon.ico',
                                   mimetype='image/vnd.microsft.icon')

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route("/cmd", methods=['POST'])
    def cmd():
        MACROS.CMD = None
        MACROS.TEXT = ""
        MACROS.TEMP = None
        value = request.form["value"]
        if not value:
            return jsonify({"text":""})
        try:
            try:
                exec(f"MACROS.TEMP = {value}", globals())
                if MACROS.TEMP is not None:
                    MACROS.TEXT += f"{MACROS.TEMP}"
            except SyntaxError:
                exec(value, globals())
            return jsonify({"text":MACROS.TEXT, "cmd":MACROS.CMD})
        except:
            return jsonify({"text":f"{traceback.format_exc()}"})

    MACROS.APP = app
    app.json_encoder = MACROS.JSONEncoder
    webbrowser.open("http://127.0.0.1:10696", 2)
    app.run(port=10696)