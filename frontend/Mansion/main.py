# -*- coding: utf-8 -*-
import webapp2

from get_how_much import GetHowMuchHandler
from get_how_much2 import GetHowMuch2Handler
from error_rate import GetErrorRateHandler

APP = webapp2.WSGIApplication([
    ('/howmuch', GetHowMuchHandler),
    ('/howmuch2', GetHowMuch2Handler),
    ('/error_rate', GetErrorRateHandler)
], debug=True)
