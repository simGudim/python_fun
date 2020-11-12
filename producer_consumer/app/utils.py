from app import db
from app.models import Msg
import datetime
import json
import requests as reqs
from sqlalchemy import func

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def db_insert(data):
    try:
        msg = json.loads(data)["msg_num"]
        delivery_time = datetime.datetime.now() - datetime.datetime\
            .strptime(json.loads(data)["start"], '%Y-%m-%d %H:%M:%S.%f')
        delivery_time = float(delivery_time.microseconds / 1000)
        msg = Msg(msg_num = msg, time = delivery_time)
        db.session.add(msg)
        db.session.commit()
    except:
        raise Exception("something went wrong!")