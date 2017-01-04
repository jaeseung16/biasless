import logging
import json
import urllib2

from google.appengine.ext import ndb

# Class for Comment

class Comment2(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    user_id = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    article_id = ndb.StringProperty(required = True)
    comment = ndb.StringProperty(required = True) # Maximum length of a comment = 1500 bytes

    def as_dict(self):
        time_fmt = '%c'
        d = {'user_id': self.user_id, 'username': self.username, 'article_id': self.article_id, 'created': self.created.strftime(time_fmt), 'comment': self.comment}
        return d
