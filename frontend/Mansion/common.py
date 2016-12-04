# -*- coding: utf-8 -*-
import json
import webapp2
from datetime import datetime
from google.appengine.ext import db

import consts


class Count(db.Model):
    count_of_howmuch = db.IntegerProperty(required=True)
    date = db.DateProperty(required=True)


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        # time.sleep(1)
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(r))


def check_access_count():
    today = datetime.today().date()
    a = Count.all()
    a.filter('date = ', today)
    for b in a.run():
        b.count_of_howmuch += 1
        b.put()
        print('count_of_howmuch = ' + str(b.count_of_howmuch))
        print('date = ' + str(b.date))
        return consts.MAX_COUNT_PER_DAY > b.count_of_howmuch

    if a.count() == 0:
        print(str(today))
        e = Count(count_of_howmuch=0, date=today)
        e.put()
    return True


class ErrorRateCache(db.Model):
    error_rates = db.ByteStringProperty(required=True)
    date = db.DateProperty(required=True)


def get_error_rate_cache(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    a = ErrorRateCache.all()
    a.filter('date = ', date)
    for b in a.run():
        return json.loads(b.error_rates)
    return None


def set_error_rate(error_rate, date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    e = ErrorRateCache(error_rates=json.dumps(error_rate), date=date)
    e.put()
