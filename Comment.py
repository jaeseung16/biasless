import logging
import json
import urllib2

from google.appengine.ext import ndb

# Class for Comment

class Comment(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    user_id = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    post_id = ndb.StringProperty(required = True)
    comment = ndb.StringProperty(required = True) # Maximum length of a comment = 1500 bytes
    score = ndb.StringProperty(required = True)
    total_score = ndb.FloatProperty(required = True)
    no_scored = ndb.IntegerProperty(required = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'user_id': self.user_id, 'username': self.username, 'post_id': self.post_id, 'created': self.created.strftime(time_fmt), 'comment': self.comment, 'score': self.score}
        return d
