from MainPage import *
from Signup import *
from Login import *
from Logout import *
from NewPost import *
from PostPage import *

from google.appengine.ext import db
from google.appengine.api import memcache

app = webapp2.WSGIApplication([('/?(?:.json)?', MainPage),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/newpost', NewPost),
                               ('/post/([0-9]+)(?:.json)?', PostPage)],
                              debug = True)
