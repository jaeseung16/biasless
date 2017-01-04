import logging
import json
import urllib2

from google.appengine.ext import ndb

# Class for Comment

class Score(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    user_id = ndb.StringProperty(required = True)
    article_id = ndb.StringProperty(required = True)
    score = ndb.FloatProperty(required = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'user_id': self.user_id, 'article_id': self.article_id, 'created': self.created.strftime(time_fmt), 'score': self.score}
        return d
