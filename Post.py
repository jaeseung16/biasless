import logging
import json
import urllib2

from google.appengine.ext import ndb

from NewsArticle import *

# Class for Post
class Post(ndb.Model):
    # Title & Date and Time for a post
    title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add = True)

    # Links to articles and images
    articles = ndb.StructuredProperty(NewsArticle, repeated = True)
    articlesID = ndb.StringProperty(repeated = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'title': self.title, 'created': self.created.strftime(time_fmt), 'articles': [a.as_dict() for a in self.articles]}
        return d
