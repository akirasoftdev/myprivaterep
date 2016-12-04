# -*- coding: utf-8 -*-
import webapp2

from get_how_much import GetHowMuchHandler
from error_rate import GetErrorRateHandler

APP = webapp2.WSGIApplication([
    ('/howmuch', GetHowMuchHandler),
    ('/error_rate', GetErrorRateHandler)
], debug=True)
