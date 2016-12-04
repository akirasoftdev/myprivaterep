# -*- coding: utf-8 -*-
import json

import common
import consts
from google.appengine.api import urlfetch

class GetErrorRateHandler(common.RestHandler):
    def get(self):
        cls = GetErrorRateHandler
        try:
            last_modified = self.request.get('lastModified')

            cached = common.get_error_rate_cache(last_modified)
            if cached != None:
                print("use cached")
                self.response.headers['content-type'] = 'application/json'
                self.response.write(json.dumps(cached))
                return

            urls = consts.HOST + 'error_rate?lastModified=' + last_modified

            headers = {'Content-Type': 'application/json'}

            result = urlfetch.fetch(urls,
                method=urlfetch.GET,
                headers=headers,
                deadline=60)

            if result.status_code == 200:
                print(type(result.content))
                common.set_error_rate(result.content, last_modified)
                self.response.headers['content-type'] = 'application/json'
                self.response.write(json.dumps(result.content))
            else:
                self.response.status_int = result.status_code
                self.response.write('URL returned status code {}'.format(result.status_code))

        except urlfetch.DownloadError:
            self.response.status_int = 500
            self.response.write('Error fetching URL')