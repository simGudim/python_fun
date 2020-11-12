
from app import app, db
from app.models import Msg
from app.utils import *
import datetime
import json
from flask import render_template, request, redirect, url_for
from sqlalchemy import func, desc
import time





@app.route('/')
@app.route('/index')
def index():
    user = {'msg': 'dcshapiro!'}
    max_msg = db.session.query(func.max(Msg.msg_num)).scalar()
    avg_time = db.session.query.filter(Msg.timestamp >= datetime.datetime.now() - datetime.timedelta(seconds=10))\
        .with_entities(func.avg(Msg.timestamp))
        .scalar()
    return render_template('index.html', title='Home', user=user, max_msg = max_msg)


## The consumer routess
@app.route('/consumer', methods=["POST"])
def consumer():
    if request.method == "POST":
        job = app.task_queue.enqueue(db_insert, request.data)
        return (f"The request was completed, job number {job}", 204)
    else:
        return "The request method has to be POST"

##The producer routes
@app.route('/producer', methods = ["GET", "POST"])
def producer():
    url = "http://localhost:5000/consumer"
    headers = {'content-type': 'application/json'}
    for i in range(0, request.form["num_calls"]):
        start = datetime.datetime.now()
        data = { "msg_num": i, "start" : start}
        reqs.post(url, data=json.dumps(data, default = myconverter), headers=headers)
    return redirect(url_for("index"))

