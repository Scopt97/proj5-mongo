"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""


import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import config

app = Flask(__name__)
CONFIG = config.configuration()

#TODO delete from cred.ini: MONGO_URL = CONFIG.MONGO_URL
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)#TODO, connect=False)  #TODO MONGO_URL)  #TODO os.environ['DB_PORT_27017_TCP_ADDR'], 27017, connect=False)
db = client.tododb



# Start code from flask_brevets.py

import flask
#from flask import request  # Already imported above
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
#import config

import logging

###
# Globals
###
#app = flask.Flask(__name__)  # Already assigned above
#CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brev', type=float)
    start_date = request.args.get('date', type=str)
    start_time = request.args.get('time', type=str)
    print("*********", request.args)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    start_iso = start_date + 'T' + start_time + ':00'
    print("***start_iso: ", start_iso)
    open_time = acp_times.open_time(km, brevet_dist, start_iso)
    close_time = acp_times.close_time(km, brevet_dist, start_iso)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

# End code from flask_brevets.py



@app.route('/todo', methods=['POST'])  # Changed from '/'
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)

@app.route('/new')  #TODO removed methods=['POST']
def new():
    mi = request.args.get('mi', type=str)
    km = request.args.get('km', type=str)
    loc = request.args.get('loc', type=str)
    open_time = request.args.get('open', type=str)
    close_time = request.args.get('close', type=str)

    name = "Control point at " + mi + "mi/" + km + "km"
    if loc == "Optional location name":  # If the location is the placeholder, don't include it
        desc = "Open time: " + open_time + " | Close time: " + close_time
    else:
        desc = "Location: " + loc + " | Open time: " + open_time + " | Close time: " + close_time

    item_doc = {
        'name': name, #request.form['name'],
        'description': desc #request.form['description']
    }

    db.tododb.insert_one(item_doc)

    return "Something" #TODO redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(port=CONFIG.PORT, host='0.0.0.0', debug=True)
