# -*- coding: utf-8 -*-
import json
from datetime import datetime

import webapp2
from google.appengine.ext import db

MAX_COUNT_PER_DAY = 10000


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


def check_access_count(self):
    today = datetime.today().date()
    a = Count.all()
    a.filter('date = ', today)
    for b in a.run():
        b.count_of_howmuch += 1
        b.put()
        print('count_of_howmuch = ' + str(b.count_of_howmuch))
        print('date = ' + str(b.date))
        return MAX_COUNT_PER_DAY > b.count_of_howmuch

    if a.count() == 0:
        print(str(today))
        e = Count(count_of_howmuch=0, date=today)
        e.put()
    return True
