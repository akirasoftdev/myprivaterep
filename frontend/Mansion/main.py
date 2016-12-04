# -*- coding: utf-8 -*-
import webapp2

from frontend.Manshion.get_how_much import QueryHandler

APP = webapp2.WSGIApplication([
    ('/howmuch', QueryHandler),
], debug=True)
