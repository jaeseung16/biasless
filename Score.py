import logging
import json
import urllib2

from google.appengine.ext import db

# Class for Comment

class Score(db.Model):
    created = db.DateTimeProperty(auto_now_add = True)
    user_id = db.StringProperty(required = True)
    article_id = db.StringProperty(required = True)
    score = db.FloatProperty(required = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'user_id': self.user_id, 'article_id': self.article_id, 'created': self.created.strftime(time_fmt), 'score': self.score}
        return d
