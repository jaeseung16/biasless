from MainPage import *
from MainPage2 import *
from Signup import *
from Login import *
from Logout import *
from NewPost import *
from PostPage import *
from ArticlePage import *
from ScorePage import *

from google.appengine.ext import db
from google.appengine.api import memcache

app = webapp2.WSGIApplication([('/?(?:.json)?', MainPage),
                               ('/main2(?:.json)?', MainPage2),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/newpost', NewPost),
                               ('/post/([0-9]+)(?:.json)?', PostPage),
                               ('/article/([0-9]+)(?:.json)?', ArticlePage),
                               ('/score/([0-9]+)(?:.json)?', ScorePage)],
                              debug = True)
