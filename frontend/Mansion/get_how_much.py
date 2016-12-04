# -*- coding: utf-8 -*-
import json

import common
import consts
from google.appengine.api import urlfetch


class GetHowMuchHandler(common.RestHandler):

    def get(self):
        cls = GetHowMuchHandler

        if not common.check_access_count():
            self.response.status_int = 503
            self.response.write('1日のアクセス上限に達しました。しばらく時間をあけて、お試しください。')
            return

        try:
            address = self.request.get('address')
            occupied = self.request.get('occupied')
            walk = self.request.get('walk')
            year = self.request.get('year')
            urls = consts.HOST + '/howmuch' + '?address=' + address + '&occupied=' + occupied
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
