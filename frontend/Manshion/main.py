# -*- coding: utf-8 -*-
import json
import webapp2
from datetime import datetime
from google.appengine.api import urlfetch
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


class QueryHandler(RestHandler):
#    HOST = 'http://ec2-52-198-163-174.ap-northeast-1.compute.amazonaws.com:5000'
    HOST = 'http://mansion-prediction-dev.5grvpjfmbg.ap-northeast-1.elasticbeanstalk.com/'
#    HOST = 'http://192.168.1.9:5000'

    def _check_access_count(self):
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

    def get(self):
        cls = QueryHandler

        if not self._check_access_count():
            self.response.status_int = 503
            self.response.write('1日のアクセス上限に達しました。しばらく時間をあけて、お試しください。')
            return

        try:
            address = self.request.get('address')
            occupied = self.request.get('occupied')
            walk = self.request.get('walk')
            year = self.request.get('year')
            urls = cls.HOST + '/howmuch' + '?address=' + address + '&occupied=' + occupied 
            urls += '&walk=' + walk + '&year=' + year

            headers = {'Content-Type': 'application/json'}

            result = urlfetch.fetch(urls,
                method=urlfetch.GET,
                headers=headers,
                deadline=60)

            if result.status_code == 200:
                print(type(result.content))
                self.response.headers['content-type'] = 'application/json'
                self.response.write(json.dumps(result.content))
            else:
                self.response.status_int = result.status_code
                self.response.write('URL returned status code {}'.format(result.status_code))

        except urlfetch.DownloadError:
            self.response.status_int = 500
            self.response.write('Error fetching URL')


APP = webapp2.WSGIApplication([
    ('/howmuch', QueryHandler),
], debug=True)
