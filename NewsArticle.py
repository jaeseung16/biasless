import logging
import json
import urllib2

from google.appengine.ext import ndb

# Class for Comment

class NewsArticle(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    title = ndb.StringProperty(required = True)
    source = ndb.StringProperty(required = True)
    url = ndb.StringProperty(required = True)
    image = ndb.StringProperty(required = True)
    description = ndb.StringProperty()
    score = ndb.StringProperty(required = True)
    total_score = ndb.FloatProperty(required = True)
    no_scored = ndb.IntegerProperty(required = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'created': self.created.strftime(time_fmt), 'title': self.title,
            'url': self.url, 'image': self.image, 'description': self.description, 'score': self.score}
        return d
